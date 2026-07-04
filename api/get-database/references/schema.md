# get-database API skill reference

specification of input parameters, environment variables, and expected output formats for the get-database skill.

## input

### arguments

1. `database_id` (required, string): the id of the database to fetch.

### environment variables

- `NOTION_PAT` (required, string): notion integration token.

## output

stdout prints the raw JSON response returned by the [retrieve a database](https://developers.notion.com/reference/retrieve-a-database) API endpoint.
