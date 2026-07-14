---
name: notion-clone
description: download a notion page or database to a local markdown directory
---
# notion clone

## workflow
1. initializes the `notion/` working directory.
2. writes the `notion.yaml` tracking configuration file.
3. automatically triggers `notion pull` to perform the initial download.

## automation
```powershell
python skills/notion-clone/scripts/notion-clone.py <notion_id> [type]
```
