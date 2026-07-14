# update-page API skill reference

Uses Notion API version `2026-03-11`.

## input

### arguments

1. `page_id` (required, string): the id of the page to update.
2. One operation: property JSON, `--read-markdown`, `--update <old_str> <new_str>`, or `--replace <markdown>`.

### environment variables

- `NOTION_PAT` (required, string): notion integration token.

## output

stdout prints raw JSON response. Markdown responses contain `markdown`, `truncated`, and `unknown_block_ids`.
