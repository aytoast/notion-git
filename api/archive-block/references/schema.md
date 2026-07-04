# archive-block API skill reference

specification of input parameters, environment variables, and expected output formats for the archive-block skill.

## input

### arguments

1. `block_id` (required, string): the id of the block to archive or delete.

### environment variables

- `NOTION_PAT` (required, string): notion integration token.

## output

stdout prints the raw JSON response returned by the [delete a block](https://developers.notion.com/reference/delete-a-block) API endpoint.
