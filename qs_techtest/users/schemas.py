

add_user_schema = {
    "title": "Add User",
    "description": "Data for a request to add a user",
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "type": {"type": "string"},
                "attributes": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email_address": {"type": "string"},
                        "country": {"type": "string"},
                    },
                    "required": ["first_name", "last_name", "email_address"]
                }
            }
        }
    },
    "required": ["data"]
}
