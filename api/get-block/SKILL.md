---
name: get-block
description: get block metadata from the notion API.
---

# get-notion-block

use a python script to perform HTTP GET requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
python api/get-block/scripts/get-notion-block.py <block_id>
```

## guidelines

- getting a block only returns its metadata. to get its children recursively, use fetch-notion-block instead.
