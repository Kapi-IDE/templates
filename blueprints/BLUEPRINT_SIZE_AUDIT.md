# 📊 Blueprint Size Audit Report

**Date:** October 2, 2025
**Purpose:** Identify bloated blueprints with unnecessary large files

---

## 🚨 Critical Issues

### 1. **ai-governance** - 35MB of vendor assets!

**Current Size:** 303,858 tokens (Complex)
**Expected Size:** ~10,000 tokens (Simple)
**Bloat Factor:** 30x inflated

**Top Offenders:**
| File | Size | Issue |
|------|------|-------|
| `jquery.dataTables.min.js` | 2.1MB | Minified vendor library |
| `fullcalendar/js/main.js` | 674KB | Vendor library |
| `bootstrap.min.css.map` | 509KB | Source map |
| `bootstrap.min.css` | 257KB | Minified CSS |
| `boxicons.svg` | 953KB | Font file |

**Additional Bloat:**
- 14 carousel images (`carousels/*.png`) - 8.5MB total
- 6 cat demo images (`cat/*.png`) - 5.1MB total
- Multiple minified vendor libraries (Select2, ApexCharts, Peity, etc.)

**Solution:**
```bash
# Remove vendor assets (should be from npm)
rm -rf industry/ai-governance/frontend/src/components/react-dashboard-theme/assets/plugins/
rm -rf industry/ai-governance/frontend/src/components/react-dashboard-theme/assets/css/*.min.*
rm industry/ai-governance/frontend/src/components/react-dashboard-theme/assets/fonts/boxicons.svg

# Remove demo images
rm -rf industry/ai-governance/frontend/src/components/react-dashboard-theme/assets/images/carousels/
rm -rf industry/ai-governance/frontend/src/components/react-dashboard-theme/assets/images/cat/
rm -rf industry/ai-governance/frontend/src/components/react-dashboard-theme/assets/images/orders/
```

---

### 2. **modernai-education** - 6.7MB video file!

**Current Size:** 276,293 tokens (Complex)
**Expected Size:** ~22,000 tokens (Simple)
**Bloat Factor:** 12.5x inflated

**Top Offenders:**
| File | Size | Issue |
|------|------|-------|
| `party_animation.webm` | 6.7MB | **Video file in source code!** |
| `package-lock.json` | 800KB | Lock file (should be excluded) |
| `zoom.png` | 478KB | Large image |
| `robot_background.jpg` | 392KB | Duplicate image (in 2 locations) |

**Solution:**
```bash
# Move video to CDN or public folder
rm modernai-education/frontend/src/assets/party_animation.webm
# Update code to reference: /videos/party_animation.webm from public/

# Remove duplicate images
rm modernai-education/frontend/src/assets/images/robot_background.jpg
# (Keep only in public/images/)
```

---

### 3. **gamified-learning-ui** - 2.5MB of images

**Issues:**
| File | Size | Issue |
|------|------|-------|
| `robot_header.png` | 860KB | Unoptimized PNG |
| `levels.png` | 783KB | Unoptimized PNG |
| `robot_header_purple.png` | 470KB | Unoptimized PNG |
| `robot_background.jpg` | 392KB | Large background |

**Solution:**
```bash
# Optimize images with tools like:
# - imageoptim (Mac)
# - squoosh.app (web)
# - sharp (Node.js)

# Or convert PNGs to WebP:
cwebp robot_header.png -o robot_header.webp -q 80
```

---

### 4. **react-landing** - 600KB of vendor CSS

**Issues:**
| File | Size | Issue |
|------|------|-------|
| `bootstrap.css` | 190KB | Unminified Bootstrap |
| `style.css` | 155KB | Large custom CSS |
| `font-awesome.css` | 144KB | Full Font Awesome |
| `hover.css` | 129KB | Hover effects library |
| `brand-bg.png` | 116KB | Background image |

**Solution:**
```bash
# Use CDN instead of bundling
# Or use Tailwind CSS (smaller, tree-shakeable)
```

---

### 5. **fastapi-rag-starter** - 264KB lock file

**Issue:**
| File | Size | Issue |
|------|------|-------|
| `uv.lock` | 264KB | Python lock file |

**Note:** Lock files are usually excluded from analysis, but this one wasn't.

---

### 6. **healthcare-triage** - 643KB package-lock.json

**Issue:**
| File | Size | Issue |
|------|------|-------|
| `package-lock.json` | 643KB | npm lock file |

**Note:** Should be excluded from token analysis.

---

## 📋 Recommendations

### Immediate Actions:

1. **Update `analyze_blueprints.py`** to exclude:
   ```python
   EXCLUDED_FILENAMES = {
       'package-lock.json',
       'yarn.lock',
       'pnpm-lock.yaml',
       'uv.lock',
       'poetry.lock',
       'Cargo.lock',
       'go.sum',
       'Gemfile.lock',
   }

   EXCLUDED_EXTENSIONS = {
       # Add media files
       '.webm', '.mp4', '.avi', '.mov', '.mkv',
       '.mp3', '.wav', '.ogg', '.flac',

       # Add source maps
       '.map',
   }

   # Add exclusion for *.min.js and *.min.css
   def is_excluded_file(file_name: str) -> bool:
       if '.min.' in file_name:  # Catches .min.js, .min.css, etc.
           return True
       # ... existing logic
   ```

2. **Clean up ai-governance:**
   - Remove entire `react-dashboard-theme/assets/` folder
   - Use npm packages instead: `react-bootstrap`, `react-icons`, etc.
   - Expected savings: **290,000 tokens (95%)**

3. **Clean up modernai-education:**
   - Move video to CDN or public folder
   - Remove duplicate images
   - Expected savings: **254,000 tokens (92%)**

4. **Optimize images** in gamified-learning-ui:
   - Convert PNG → WebP
   - Compress with imageoptim
   - Expected savings: **1.5MB → 500KB (67%)**

5. **Use CDN for vendor libraries** in react-landing:
   - Bootstrap, Font Awesome via CDN
   - Or switch to modern alternatives (Tailwind CSS)

---

## 📊 Before/After Comparison

| Blueprint | Before | After Cleanup | Savings |
|-----------|--------|---------------|---------|
| **ai-governance** | 303,858 tokens | ~13,000 | **97% ↓** |
| **modernai-education** | 276,293 tokens | ~22,000 | **92% ↓** |
| **gamified-learning-ui** | ~15,000 tokens | ~8,000 | **47% ↓** |
| **react-landing** | ~12,000 tokens | ~5,000 | **58% ↓** |

**Total Reduction:** ~580,000 tokens → ~48,000 tokens (**92% reduction!**)

---

## ✅ Clean Blueprints (No issues found)

The following blueprints are well-optimized:

- ✅ **rag-shopping-app** - 2,264 tokens
- ✅ **cancer-detection-trainer**
- ✅ **deep-document-analysis**
- ✅ **langgraph-multi-agent**
- ✅ **nfl-play-predictor**
- ✅ **react-stock-agent**
- ✅ **url-shortener**
- ✅ **meme-generator**
- ✅ **markdown-blog**
- ✅ **simple-crm**
- ✅ **customer-feedback-analyzer**
- ✅ **enterprise-analytics-dashboard**
- ✅ **education**
- ✅ **finance-analysis**
- ✅ **legal-analysis**
- ✅ **team-knowledge-base**
- ✅ All core-apps (ai-chat-interface, habit-tracker, perplexity-clone, etc.)
- ✅ All games (racing-game, threejs-puzzle-game, threejs-racing-game)

---

## 🎯 Next Steps

1. Update `analyze_blueprints.py` with improved exclusions
2. Clean up ai-governance and modernai-education
3. Create `.blueprintignore` file pattern (like `.gitignore`)
4. Add pre-commit hook to prevent large files
5. Document asset guidelines in blueprint creation docs

---

**Result:** All blueprints should be <30,000 tokens for "Moderate" complexity, ideally <10,000 for "Simple"
