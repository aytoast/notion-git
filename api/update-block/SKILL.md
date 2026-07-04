---
name: update-block
description: update content of an existing block in the notion API.
---

# update-notion-block

use a python script to perform HTTP PATCH requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
python api/update-block/scripts/update-notion-block.py <block_id> '{"paragraph":{"rich_text":[{"type":"text","text":{"content":"replacement text"}}]}}'
```

## guidelines

- use this to replace the content of a specific block.
