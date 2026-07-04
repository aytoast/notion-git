# update-block API skill reference

specification of input parameters, environment variables, and expected output formats for the update-block skill.

## input

### arguments

1. `block_id` (required, string): the id of the block to update.
2. `json_data` (required, string): JSON representation of updated block properties.

### environment variables

- `NOTION_PAT` (required, string): notion integration token.

## output

stdout prints the raw JSON response returned by the [update a block](https://developers.notion.com/reference/patch-block) API endpoint.
