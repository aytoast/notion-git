---
name: get-page
description: get page metadata from the notion API.
---

# get-notion-page

use a python script to perform HTTP GET requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
python api/get-page/scripts/get-notion-page.py <page_id>
```

## guidelines

- notion URLs formatted as `notion.so/<32-char-id>?v=<view-id>` contain the page ID as the main path segment.
- getting a page only returns its properties and metadata. to get its content, fetch the block children instead.
