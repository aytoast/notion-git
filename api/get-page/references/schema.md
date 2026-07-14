# get-page API skill reference

specification of input parameters, environment variables, and expected output formats for the get-page skill.

## input

### arguments

1. `page_id` (required, string): the 32-character hexadecimal string representing the notion page id (e.g. `3503bb63f18e802d8edfd8466894229c`).

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

stdout prints the raw JSON response returned by the [retrieve a page](https://developers.notion.com/reference/retrieve-a-page) API endpoint.

### expected schema

```json
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
    "type": "database_id | page_id | workspace",
    "database_id": "string (optional)",
    "page_id": "string (optional)"
  },
  "in_trash": false,
  "properties": {
    "title": {
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
```
