---
name: update-page
description: read and update Notion page content through Markdown Content API; update page properties.
---

# update Notion page

Use Markdown Content API for page body changes. Script uses Notion API `2026-03-11` and resolves `NOTION_PAT` from `.env`.

## commands

```powershell
python api/update-page/scripts/update-notion-page.py <page_id> --read-markdown
python api/update-page/scripts/update-notion-page.py <page_id> --update 'old text' 'new text'
python api/update-page/scripts/update-notion-page.py <page_id> --replace @page.md
python api/update-page/scripts/update-notion-page.py <page_id> '{"properties":{"status":{"status":{"name":"done"}}}}'
```

## guidelines

- Use `--update` for targeted edits and `--replace` for full page replacement.
- Full replacement refuses child page/database deletion unless `--allow-deleting-content` is supplied.
- Use existing block skills when Markdown response is truncated or has `unknown_block_ids`.
