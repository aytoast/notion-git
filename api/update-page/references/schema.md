# update-page API skill reference

specification of input parameters, environment variables, and expected output formats for the update-page skill.

## input

### arguments

1. `page_id` (required, string): the id of the page to update.
2. `json_data` (required, string): JSON representation of updated page properties.

### environment variables

- `NOTION_PAT` (required, string): notion integration token.

## output

stdout prints the raw JSON response returned by the [update page properties](https://developers.notion.com/reference/patch-page) API endpoint.
