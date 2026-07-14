---
name: notion-push
description: push local markdown changes to Notion through Markdown Content API
---
# notion push

## workflow
1. parse local Markdown files and load `.notion-index.json` baseline Markdown.
2. send precise changes through `update_content` when changed text is unique.
3. use `replace_content` when change selection is ambiguous.
4. use block API only for pages marked as incomplete Markdown fallback.
5. automatically run `notion pull` upon completion to refresh the shadow cache.

## automation
```powershell
python skills/notion-push/scripts/notion-push.py
```
