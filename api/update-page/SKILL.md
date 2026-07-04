---
name: update-page
description: update page properties in the notion API.
---

# update-notion-page

use a python script to perform HTTP PATCH requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
python api/update-page/scripts/update-notion-page.py <page_id> '{"properties":{"status":{"status":{"name":"done"}}}}'
```

## guidelines

- use this to modify the properties of an existing page. this does not change the page content.
