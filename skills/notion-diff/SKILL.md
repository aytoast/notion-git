---
name: notion-diff
description: compare local markdown changes against the cached notion state
---
# notion diff

## workflow
1. parse local markdown files and load the `.notion-index.json` shadow cache.
2. run a diff sequence matcher to identify added, modified, and deleted blocks.
3. output a colored git-style diff preview.

## automation
```powershell
python skills/notion-diff/scripts/notion-diff.py
```
