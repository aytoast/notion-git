---
name: create-page
description: create a page in a database in the notion API.
---

# create-notion-page

use a python script to perform HTTP POST requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
python api/create-page/scripts/create-notion-page.py '{"parent":{"database_id":"<database_id>"},"properties":{"Name":{"title":[{"text":{"content":"<title_text>"}}]}}}'
```

## guidelines

- use this to create new records in a database.
- to link to another notion page inside rich_text, use a mention block:
```json
{
  "type": "mention",
  "mention": {
    "type": "page",
    "page": { "id": "<target_page_id>" }
  }
}
```
