# get-block-children API skill reference

specification of input parameters, environment variables, and expected output formats for the get-block-children skill.

## input

### arguments

1. `block_id` (required, string): the 32-character hexadecimal string representing the notion page or block id (e.g. `3503bb63f18e802d8edfd8466894229c`).

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

stdout prints the raw JSON response returned by the [retrieve block children](https://developers.notion.com/reference/retrieve-a-block-with-children) API endpoint.

### expected schema

```json
{
  "object": "list",
  "results": [
    {
      "object": "block",
      "id": "string",
      "parent": {
        "type": "page_id",
        "page_id": "string"
      },
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
      "has_children": false,
      "in_trash": false,
      "type": "paragraph | heading_1 | heading_2 | heading_3 | bulleted_list_item | numbered_list_item | child_page | child_database",
      "paragraph": {
        "rich_text": [
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
        ],
        "color": "default"
      }
    }
  ],
  "next_cursor": null,
  "has_more": false,
  "type": "block",
  "block": {}
}
```
