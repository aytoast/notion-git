---
name: query-database
description: query a database with or without filters in the notion API.
---

# query-notion-database

use a python script to perform HTTP POST requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
# query with filters
python api/query-database/scripts/query-notion-database.py <database_id> '{"filter":{"property":"status","status":{"equals":"ready"}},"page_size":25}'

# query without filters
python api/query-database/scripts/query-notion-database.py <database_id> "{}"
```

## guidelines

- use this to search for specific pages within a database.
- always provide a valid JSON payload in the request body.
