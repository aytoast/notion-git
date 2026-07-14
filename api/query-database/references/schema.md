# query-database API skill reference

specification of input parameters, environment variables, and expected output formats for the query-database skill.

## input

### arguments

1. `database_id` (required, string): the 32-character hexadecimal string representing the notion database id (e.g. `3503bb63f18e81cda3b0cf116d01ee23`).
2. `json_data` (optional, string): the JSON query payload containing filtering, sorting, or pagination criteria (defaults to `{}`). if prefixed with `@`, reads from the specified file path; if `-`, reads from stdin.

### environment variables

one of the following token variables must be defined to authenticate with the notion API:
- `NOTION`
- `NOTION_PERSONAL`
- `NOTION_STONE`
- `NOTION_TOKEN`
- `NOTION_API_KEY`
- `NOTION_PAT`
- `NOTION_INTEGRATION_TOKEN`
- `NOTION_SECRET`

## output

stdout prints the raw JSON response returned by the [query a database](https://developers.notion.com/reference/post-database-query) API endpoint.

### expected schema

```json
{
  "object": "list",
  "results": [
    {
      "object": "page",
      "id": "string",
      "created_time": "string (ISO 8601)",
      "last_edited_time": "string (ISO 8601)",
      "created_by": {
        "object": "user",
        "id": "string"
      },
      "last_edited_by": {
        "object": "user",
        "id": "string"
      },
      "cover": null,
      "icon": null,
      "parent": {
        "type": "database_id",
        "database_id": "string"
      },
      "in_trash": false,
      "properties": {
        "Name": {
          "id": "title",
          "type": "title",
          "title": [
            {
              "type": "text",
              "text": {
                "content": "string",
                "link": null
              },
              "annotations": {
                "bold": false,
                "italic": false,
                "strikethrough": false,
                "underline": false,
                "code": false,
                "color": "default"
              },
              "plain_text": "string",
              "href": null
            }
          ]
        }
      },
      "url": "string"
    }
  ],
  "next_cursor": null,
  "has_more": false,
  "type": "page",
  "page": {}
}
```
