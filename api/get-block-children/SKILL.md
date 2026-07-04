---
name: get-block-children
description: get block children from the notion API.
---

# get-notion-block-children

use a python script to perform HTTP GET requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
python api/get-block-children/scripts/get-notion-block-children.py <block_id>
```

## guidelines

- notion URLs formatted as `notion.so/<32-char-id>?v=<view-id>` contain the page ID as the main path segment.
- getting block children retrieves the content blocks of a page.
