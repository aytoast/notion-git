# append-block-children API skill reference

specification of input parameters, environment variables, and expected output formats for the append-block-children skill.

## input

### arguments

1. `block_id` (required, string): the parent page or block id to append children under.
2. `json_data` (required, string): the children blocks payload as JSON.

### environment variables

- `NOTION_PAT` (required, string): notion integration token.

## output

stdout prints the raw JSON response returned by the [append block children](https://developers.notion.com/reference/patch-block-children) API endpoint.
