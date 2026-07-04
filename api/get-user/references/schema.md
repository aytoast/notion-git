# get-user API skill reference

specification of input parameters, environment variables, and expected output formats for the get-user skill.

## input

### arguments

(none required)

### environment variables

- `NOTION_PAT` (required, string): notion integration token.

## output

stdout prints the raw JSON response returned by the [retrieve bot user](https://developers.notion.com/reference/get-self) API endpoint.
