---
name: append-block-children
description: append child blocks under a parent block or page in the notion API.
---

# append-notion-block-children

use a python script to perform HTTP PATCH requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
python api/append-block-children/scripts/append-notion-block-children.py <block_id> '{"children":[{"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":"new child block"}}]}}]}'
```

## guidelines

- use this to add new content to a page or nested content inside another block.
- a page is technically a block, so its page ID can be used as the block ID here.
