# get-block API skill reference

specification of input parameters, environment variables, and expected output formats for the get-block skill.

## input

### arguments

1. `block_id` (required, string): the id of the block to fetch.

### environment variables

- `NOTION_PAT` (required, string): notion integration token.

## output

stdout prints the raw JSON response returned by the [retrieve a block](https://developers.notion.com/reference/retrieve-a-block) API endpoint.
