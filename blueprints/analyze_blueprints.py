#!/usr/bin/env python3
"""
Blueprint Size Analyzer - Track complexity and size metrics for KAPI blueprint templates.

This tool analyzes blueprint repositories to ensure they stay within complexity/size targets
for efficient deployment and token usage. Designed for the quick-wins blueprint catalog.

Usage:
    python analyze_blueprints.py                    # Analyze all blueprints
    python analyze_blueprints.py -b practica-clean  # Analyze specific blueprint
    python analyze_blueprints.py --csv              # Export CSV format
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

# --- Configuration ---

# Excluded directories (common build/dependency artifacts)
EXCLUDED_DIRS = {
    "node_modules", ".git", ".svn", "__pycache__", "venv", ".venv", "env",
    "dist", "build", "out", "target", "*.egg-info", ".vscode", ".idea",
    "vendor", "site-packages", ".terraform", ".serverless", "coverage",
    "logs", "temp", "tmp", ".next", ".nuxt", ".cache", "bin", "obj",
    "bower_components", "jspm_packages", ".bundle", ".gradle", ".mvn"
}

# Excluded file extensions (non-code/binary files)
EXCLUDED_EXTENSIONS = {
    # Data/config
    '.csv', '.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.conf',
    # Documentation
    '.txt', '.md', '.rst', '.adoc', '.pdf', '.doc', '.docx',
    # Binaries/Archives
    '.bin', '.dat', '.db', '.sqlite', '.sqlite3',
    '.zip', '.tar', '.gz', '.bz2', '.rar', '.7z', '.jar', '.war',
    '.exe', '.dll', '.so', '.dylib', '.pyc', '.pyo', '.o', '.a', '.obj', '.class',
    # Media
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp',
    '.mp3', '.wav', '.mp4', '.avi', '.mov', '.mkv',
    # Misc
    '.lock', '.sum', '.icns', '.ttf', '.otf', '.woff', '.woff2', '.log',
    '.DS_Store'
}

# Code file extensions to track separately (for code vs config metrics)
CODE_EXTENSIONS = {
    # JavaScript/TypeScript
    '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
    # Python
    '.py', '.pyx',
    # Go
    '.go',
    # Java
    '.java',
    # C#
    '.cs', '.cshtml', '.razor',
    # Other
    '.rb', '.php', '.swift', '.kt', '.rs', '.c', '.cpp', '.h', '.hpp'
}

# Config file extensions (important but not source code)
CONFIG_EXTENSIONS = {
    '.json', '.yaml', '.yml', '.toml', '.ini', '.env', '.config',
    '.xml', '.properties', '.conf'
}

# Excluded filenames
EXCLUDED_FILENAMES = {
    '.ds_store', 'thumbs.db', 'desktop.ini', 'package-lock.json',
    'yarn.lock', 'pnpm-lock.yaml', 'go.sum', 'Gemfile.lock', 'Cargo.lock'
}

# --- Tokenizer Setup ---
try:
    import tiktoken
    encoding = tiktoken.get_encoding("cl100k_base")
    TOKENIZER_METHOD = "tiktoken (cl100k_base)"

    def count_tokens(content: str) -> int:
        try:
            tokens = encoding.encode(content, disallowed_special=())
            return len(tokens)
        except Exception as e:
            print(f"Warning: tiktoken encoding failed: {e}", file=sys.stderr)
            return 0
except ImportError:
    TOKENIZER_METHOD = "whitespace split (install tiktoken for accuracy)"

    def count_tokens(content: str) -> int:
        return len(content.split())

# --- Data Models ---

@dataclass
class FileMetrics:
    """Metrics for a single file."""
    path: str
    size_bytes: int
    lines: int
    tokens: int
    file_type: str  # 'code', 'config', 'other'

@dataclass
class BlueprintMetrics:
    """Complete metrics for a blueprint."""
    name: str
    path: str
    total_files: int
    total_size_mb: float
    total_lines: int
    total_tokens: int

    # Breakdown by type
    code_files: int
    code_lines: int
    code_tokens: int

    config_files: int
    config_lines: int

    # Top files
    top_files_by_tokens: List[Dict]
    top_files_by_size: List[Dict]

    # Metadata
    detected_stack: List[str]
    complexity_score: str  # 'Simple', 'Moderate', 'Complex'

# --- Helper Functions ---

def is_excluded_dir(dir_name: str) -> bool:
    """Check if directory should be excluded."""
    if dir_name in EXCLUDED_DIRS:
        return True
    if "*.egg-info" in EXCLUDED_DIRS and dir_name.endswith(".egg-info"):
        return True
    return False

def is_excluded_file(file_name: str) -> bool:
    """Check if file should be excluded."""
    if file_name.lower() in EXCLUDED_FILENAMES:
        return True
    _, ext = os.path.splitext(file_name)
    return ext.lower() in EXCLUDED_EXTENSIONS

def get_file_type(file_name: str) -> str:
    """Determine file type: code, config, or other."""
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()

    if ext in CODE_EXTENSIONS:
        return 'code'
    elif ext in CONFIG_EXTENSIONS:
        return 'config'
    else:
        return 'other'

def count_lines(file_path: str) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except:
        return 0

def analyze_file(file_path: str) -> FileMetrics:
    """Analyze a single file and return metrics."""
    try:
        size = os.path.getsize(file_path)

        # Read content for token counting
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        lines = content.count('\n') + 1
        tokens = count_tokens(content)
        file_type = get_file_type(os.path.basename(file_path))

        return FileMetrics(
            path=file_path,
            size_bytes=size,
            lines=lines,
            tokens=tokens,
            file_type=file_type
        )
    except Exception as e:
        print(f"Warning: Error analyzing {file_path}: {e}", file=sys.stderr)
        return FileMetrics(file_path, 0, 0, 0, 'error')

def detect_stack(blueprint_path: str) -> List[str]:
    """Detect technology stack from files present."""
    stack = []

    # Check for package managers and config files
    if (Path(blueprint_path) / 'package.json').exists():
        stack.append('Node.js')
        if (Path(blueprint_path) / 'tsconfig.json').exists():
            stack.append('TypeScript')

    if (Path(blueprint_path) / 'go.mod').exists():
        stack.append('Go')

    if (Path(blueprint_path) / 'requirements.txt').exists() or \
       (Path(blueprint_path) / 'pyproject.toml').exists():
        stack.append('Python')

    if (Path(blueprint_path) / 'pom.xml').exists() or \
       (Path(blueprint_path) / 'build.gradle').exists():
        stack.append('Java')

    if any((Path(blueprint_path) / f).exists() for f in ['*.csproj', '*.sln']):
        stack.append('C#')

    # Check for frameworks
    if (Path(blueprint_path) / 'next.config.js').exists():
        stack.append('Next.js')
    if (Path(blueprint_path) / 'vite.config.ts').exists():
        stack.append('Vite')

    return stack if stack else ['Unknown']

def calculate_complexity(metrics: BlueprintMetrics) -> str:
    """Calculate complexity score based on metrics."""
    # Simple heuristics
    if metrics.total_tokens < 10000 and metrics.code_files < 20:
        return 'Simple'
    elif metrics.total_tokens < 30000 and metrics.code_files < 50:
        return 'Moderate'
    else:
        return 'Complex'

# --- Main Analysis ---

def analyze_blueprint(blueprint_path: str, blueprint_name: str = None) -> BlueprintMetrics:
    """Analyze a single blueprint directory."""
    if blueprint_name is None:
        blueprint_name = os.path.basename(blueprint_path)

    print(f"Analyzing: {blueprint_name}...", file=sys.stderr)

    file_metrics: List[FileMetrics] = []

    # Walk directory
    for dirpath, dirnames, filenames in os.walk(blueprint_path, topdown=True):
        # Filter excluded directories
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]

        # Analyze files
        for filename in filenames:
            if is_excluded_file(filename):
                continue

            file_path = os.path.join(dirpath, filename)
            metrics = analyze_file(file_path)
            file_metrics.append(metrics)

    # Aggregate metrics
    total_files = len(file_metrics)
    total_size = sum(f.size_bytes for f in file_metrics)
    total_lines = sum(f.lines for f in file_metrics)
    total_tokens = sum(f.tokens for f in file_metrics)

    code_files = [f for f in file_metrics if f.file_type == 'code']
    config_files = [f for f in file_metrics if f.file_type == 'config']

    # Top files
    top_by_tokens = sorted(file_metrics, key=lambda f: f.tokens, reverse=True)[:5]
    top_by_size = sorted(file_metrics, key=lambda f: f.size_bytes, reverse=True)[:5]

    # Detect stack
    stack = detect_stack(blueprint_path)

    # Create metrics object
    metrics = BlueprintMetrics(
        name=blueprint_name,
        path=blueprint_path,
        total_files=total_files,
        total_size_mb=round(total_size / (1024 * 1024), 2),
        total_lines=total_lines,
        total_tokens=total_tokens,
        code_files=len(code_files),
        code_lines=sum(f.lines for f in code_files),
        code_tokens=sum(f.tokens for f in code_files),
        config_files=len(config_files),
        config_lines=sum(f.lines for f in config_files),
        top_files_by_tokens=[
            {'path': f.path, 'tokens': f.tokens} for f in top_by_tokens
        ],
        top_files_by_size=[
            {'path': f.path, 'size_mb': round(f.size_bytes / (1024*1024), 2)}
            for f in top_by_size
        ],
        detected_stack=stack,
        complexity_score='Unknown'
    )

    # Calculate complexity
    metrics.complexity_score = calculate_complexity(metrics)

    return metrics

def format_output_table(all_metrics: List[BlueprintMetrics]) -> str:
    """Format metrics as a markdown table."""
    lines = []
    lines.append("# Blueprint Size Analysis Report\n")
    lines.append(f"**Tokenizer:** {TOKENIZER_METHOD}\n")
    lines.append("## Summary Table\n")

    # Header
    lines.append("| Blueprint | Stack | Files | Size (MB) | Code Lines | Total Tokens | Complexity |")
    lines.append("|-----------|-------|-------|-----------|------------|--------------|------------|")

    # Sort by tokens (descending)
    sorted_metrics = sorted(all_metrics, key=lambda m: m.total_tokens, reverse=True)

    for m in sorted_metrics:
        stack_str = ', '.join(m.detected_stack[:2])  # First 2 stacks
        lines.append(
            f"| {m.name} | {stack_str} | {m.total_files} | {m.total_size_mb} | "
            f"{m.code_lines:,} | {m.total_tokens:,} | {m.complexity_score} |"
        )

    # Totals
    total_files = sum(m.total_files for m in all_metrics)
    total_size = sum(m.total_size_mb for m in all_metrics)
    total_tokens = sum(m.total_tokens for m in all_metrics)

    lines.append(f"| **TOTAL** | - | {total_files} | {total_size:.2f} | - | {total_tokens:,} | - |")

    # Detailed breakdown
    lines.append("\n## Detailed Breakdown\n")

    for m in sorted_metrics:
        lines.append(f"\n### {m.name}")
        lines.append(f"- **Path:** `{m.path}`")
        lines.append(f"- **Stack:** {', '.join(m.detected_stack)}")
        lines.append(f"- **Complexity:** {m.complexity_score}")
        lines.append(f"- **Total Files:** {m.total_files}")
        lines.append(f"- **Code Files:** {m.code_files} ({m.code_lines:,} lines, {m.code_tokens:,} tokens)")
        lines.append(f"- **Config Files:** {m.config_files} ({m.config_lines:,} lines)")
        lines.append(f"- **Total Size:** {m.total_size_mb} MB")
        lines.append(f"- **Total Tokens:** {m.total_tokens:,}")

        if m.top_files_by_tokens:
            lines.append(f"\n**Top 5 Files by Token Count:**")
            for i, f in enumerate(m.top_files_by_tokens, 1):
                rel_path = f['path'].replace(m.path, '').lstrip('/')
                lines.append(f"{i}. `{rel_path}` - {f['tokens']:,} tokens")

    return '\n'.join(lines)

def format_output_csv(all_metrics: List[BlueprintMetrics]) -> str:
    """Format metrics as CSV."""
    lines = []
    lines.append("Blueprint,Stack,Files,Size_MB,Code_Lines,Total_Tokens,Complexity")

    for m in all_metrics:
        stack = ' '.join(m.detected_stack)
        lines.append(f'"{m.name}","{stack}",{m.total_files},{m.total_size_mb},'
                    f'{m.code_lines},{m.total_tokens},{m.complexity_score}')

    return '\n'.join(lines)

# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="Analyze KAPI blueprint templates for size and complexity metrics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all blueprints in quick-wins directory
  python analyze_blueprints.py

  # Analyze specific blueprint
  python analyze_blueprints.py -b practica-clean-architecture

  # Export to CSV
  python analyze_blueprints.py --csv -o blueprints.csv

  # Export to JSON
  python analyze_blueprints.py --json -o blueprints.json
        """
    )

    parser.add_argument(
        '-d', '--directory',
        default='.',
        help='Root directory containing blueprints (default: current directory)'
    )
    parser.add_argument(
        '-b', '--blueprint',
        help='Analyze specific blueprint by name'
    )
    parser.add_argument(
        '--csv',
        action='store_true',
        help='Output in CSV format'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)'
    )

    args = parser.parse_args()

    root_dir = os.path.abspath(args.directory)

    if not os.path.isdir(root_dir):
        print(f"Error: Directory not found: {root_dir}", file=sys.stderr)
        sys.exit(1)

    # Find blueprints to analyze
    blueprints_to_analyze = []

    if args.blueprint:
        # Specific blueprint
        blueprint_path = os.path.join(root_dir, args.blueprint)
        if not os.path.isdir(blueprint_path):
            print(f"Error: Blueprint not found: {blueprint_path}", file=sys.stderr)
            sys.exit(1)
        blueprints_to_analyze.append((blueprint_path, args.blueprint))
    else:
        # All subdirectories (excluding common non-blueprint dirs)
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}
        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            if os.path.isdir(item_path) and item not in skip_dirs and not item.startswith('.'):
                blueprints_to_analyze.append((item_path, item))

    if not blueprints_to_analyze:
        print("No blueprints found to analyze.", file=sys.stderr)
        sys.exit(1)

    # Analyze each blueprint
    all_metrics = []
    for bp_path, bp_name in blueprints_to_analyze:
        metrics = analyze_blueprint(bp_path, bp_name)
        all_metrics.append(metrics)

    # Generate output
    if args.json:
        output = json.dumps([asdict(m) for m in all_metrics], indent=2)
    elif args.csv:
        output = format_output_csv(all_metrics)
    else:
        output = format_output_table(all_metrics)

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(output)

if __name__ == "__main__":
    main()
