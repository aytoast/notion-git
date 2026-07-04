---
name: get-database
description: get database metadata from the notion API.
---

# get-notion-database

use a python script to perform HTTP GET requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
python api/get-database/scripts/get-notion-database.py <database_id>
```

## guidelines

- notion URLs formatted as `notion.so/<32-char-id>?v=<view-id>` contain the database ID as the main path segment.
