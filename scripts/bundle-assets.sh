#!/bin/bash

#
# KAPI Templates Asset Bundling Script
#
# This script:
# 1. Creates .tar.zst bundles for all blueprints and components
# 2. Generates unified catalog.json manifest with checksums
#
# Usage: ./scripts/bundle-assets.sh
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🎁 KAPI Templates Asset Bundling"
echo "================================="
echo ""
echo "📂 Templates root: $TEMPLATES_ROOT"
echo ""

cd "$TEMPLATES_ROOT"

# Check if tar supports zst compression
if ! tar --version | grep -q "zstd"; then
  echo "⚠️  Warning: tar doesn't support zstd compression"
  echo "   Using gzip (.tar.gz) instead"
  COMPRESSION="gz"
  BUNDLE_EXT="tar.gz"
  TAR_FLAGS="-czf"
else
  COMPRESSION="zst"
  BUNDLE_EXT="tar.zst"
  TAR_FLAGS="-I zstd -cf"
fi

echo "🔧 Using compression: $COMPRESSION ($BUNDLE_EXT)"
echo ""

# Counter for bundled assets
BUNDLED_BLUEPRINTS=0
BUNDLED_COMPONENTS=0
SKIPPED=0

#
# Bundle all blueprints
#
echo "📦 Bundling blueprints..."
echo ""

if [ -d "blueprints" ]; then
  # Find all directories with metadata.yaml
  find blueprints -name "metadata.yaml" -type f | while read -r metadata_file; do
    blueprint_dir="$(dirname "$metadata_file")"
    blueprint_name="$(basename "$blueprint_dir")"
    bundle_file="$blueprint_dir/bundle.$BUNDLE_EXT"

    echo "  → $blueprint_dir"

    # Create bundle (exclude existing bundles, .git, node_modules)
    (
      cd "$blueprint_dir"
      tar $TAR_FLAGS bundle.$BUNDLE_EXT \
        --exclude="bundle.tar.*" \
        --exclude=".git" \
        --exclude="node_modules" \
        --exclude=".next" \
        --exclude="dist" \
        --exclude="build" \
        --exclude=".DS_Store" \
        . 2>/dev/null || true
    )

    if [ -f "$bundle_file" ]; then
      size=$(du -h "$bundle_file" | cut -f1)
      echo "     ✅ Bundle created: $size"
      BUNDLED_BLUEPRINTS=$((BUNDLED_BLUEPRINTS + 1))
    else
      echo "     ⚠️  Bundle failed"
      SKIPPED=$((SKIPPED + 1))
    fi
  done
else
  echo "  ⚠️  blueprints/ directory not found"
fi

echo ""
echo "📦 Bundling components..."
echo ""

if [ -d "components" ]; then
  # Find all component directories with metadata.yaml or README.md
  find components -type d | while read -r component_dir; do
    # Skip the root components directory
    if [ "$component_dir" = "components" ]; then
      continue
    fi

    # Check if this directory has metadata.yaml or README.md
    if [ -f "$component_dir/metadata.yaml" ] || [ -f "$component_dir/README.md" ]; then
      component_name="$(basename "$component_dir")"
      bundle_file="$component_dir/bundle.$BUNDLE_EXT"

      echo "  → $component_dir"

      # Create bundle
      (
        cd "$component_dir"
        tar $TAR_FLAGS bundle.$BUNDLE_EXT \
          --exclude="bundle.tar.*" \
          --exclude=".git" \
          --exclude="node_modules" \
          --exclude=".DS_Store" \
          . 2>/dev/null || true
      )

      if [ -f "$bundle_file" ]; then
        size=$(du -h "$bundle_file" | cut -f1)
        echo "     ✅ Bundle created: $size"
        BUNDLED_COMPONENTS=$((BUNDLED_COMPONENTS + 1))
      else
        echo "     ⚠️  Bundle failed"
        SKIPPED=$((SKIPPED + 1))
      fi
    fi
  done
else
  echo "  ⚠️  components/ directory not found"
fi

echo ""
echo "📝 Generating catalog.json..."
echo ""

# Check if Node.js is available
if ! command -v node &> /dev/null; then
  echo "❌ Node.js not found. Cannot generate catalog.json"
  echo "   Please install Node.js and try again"
  exit 1
fi

# Check if js-yaml is installed
if ! node -e "require('js-yaml')" 2>/dev/null; then
  echo "📦 Installing js-yaml dependency..."
  npm install --no-save js-yaml 2>/dev/null || {
    echo "⚠️  Failed to install js-yaml. Trying yarn..."
    yarn add js-yaml --dev 2>/dev/null || {
      echo "❌ Cannot install js-yaml. Please install manually:"
      echo "   npm install --save-dev js-yaml"
      exit 1
    }
  }
fi

# Run catalog generator
node "$SCRIPT_DIR/generate-catalog.js"

# Verify catalog was created
if [ -f "catalog.json" ]; then
  CATALOG_SIZE=$(du -h catalog.json | cut -f1)
  echo ""
  echo "✅ Bundling complete!"
  echo ""
  echo "📊 Summary:"
  echo "   Blueprints bundled: $BUNDLED_BLUEPRINTS"
  echo "   Components bundled: $BUNDLED_COMPONENTS"
  echo "   Skipped/Failed: $SKIPPED"
  echo "   Catalog size: $CATALOG_SIZE"
  echo ""
  echo "📂 Output:"
  echo "   Catalog: $TEMPLATES_ROOT/catalog.json"
  echo ""
else
  echo ""
  echo "❌ Catalog generation failed"
  exit 1
fi
