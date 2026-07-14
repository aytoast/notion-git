---
name: archive-block
description: move a block to trash in the Notion API.
---

# archive-notion-block

use a python script to perform HTTP PATCH requests to the notion API. the script automatically resolves authorization tokens from the .env file.

## commands

```powershell
python api/archive-block/scripts/archive-notion-block.py <block_id>
```

## guidelines

- archiving a block effectively deletes it from view.
- a page is a block, so this command can also archive pages.
