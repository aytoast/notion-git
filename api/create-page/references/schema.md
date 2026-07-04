# create-page API skill reference

specification of input parameters, environment variables, and expected output formats for the create-page skill.

## input

### arguments

1. `json_data` (required, string): JSON representation of page parent, properties, and children.

### environment variables

- `NOTION_PAT` (required, string): notion integration token.

## output

stdout prints the raw JSON response returned by the [create a page](https://developers.notion.com/reference/post-page) API endpoint.
