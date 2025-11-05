#!/usr/bin/env python3
"""Scan templates/ for disallowed keywords or hardcoded credentials."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Iterable

TEMPLATES_DIR = pathlib.Path('templates')

# Keywords that should never ship in starter code
KEYWORD_PATTERNS: Iterable[re.Pattern[str]] = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bMitra\b",
        r"Modern\s+AI\s+Pro",
        r"Brahmasumm",
    ]
]

# Database connection strings / credentials to flag
SENSITIVE_PATTERNS: Iterable[re.Pattern[str]] = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"postgres(?:ql)?://[^'\"]+",
        r"mysql://[^'\"]+",
        r"mongodb://[^'\"]+",
        r"sqlserver://[^'\"]+",
        r"DATABASE_URL\s*=\s*['\"][^'\"]+://",
        r"password=\w+",
    ]
]

IGNORED_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.webm', '.ico', '.svg', '.avif', '.mp4', '.pdf', '.woff', '.woff2', '.ttf', '.eot', '.otf'
}

IGNORED_DIRECTORIES = {
    'node_modules',
    '.next',
    '__pycache__',
    'dist',
    'build',
    '.git',
}


def is_text_file(path: pathlib.Path) -> bool:
    return path.suffix.lower() not in IGNORED_EXTENSIONS


def scan_file(path: pathlib.Path) -> list[str]:
    findings: list[str] = []
    try:
        content = path.read_text(encoding='utf-8')
    except Exception:
        return findings

    lines = content.splitlines()
    for idx, line in enumerate(lines, start=1):
        for pattern in KEYWORD_PATTERNS:
            if pattern.search(line):
                findings.append(f"{path}:{idx}: keyword -> {line.strip()}")
                break
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(line):
                findings.append(f"{path}:{idx}: sensitive -> {line.strip()}")
                break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--templates-dir', type=pathlib.Path, default=TEMPLATES_DIR)
    args = parser.parse_args()

    templates_dir: pathlib.Path = args.templates_dir
    if not templates_dir.exists():
        print(f"Templates directory not found: {templates_dir}", file=sys.stderr)
        return 1

    all_findings: list[str] = []
    for path in templates_dir.rglob('*'):
        if any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue
        if path.is_file() and is_text_file(path):
            all_findings.extend(scan_file(path))

    if all_findings:
        print("Sensitive references detected:\n")
        for finding in all_findings:
            print(finding)
        return 1

    print("No disallowed keywords or credentials detected in templates/.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
