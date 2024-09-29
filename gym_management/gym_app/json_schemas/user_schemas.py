CREATE_SCHEMA = {
    "title": "User",
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 1,
            "maxLength": 150
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 128
        }
    },
    "required": [
        "username",
        "password"
    ]
}

UPDATE_SCHEMA = {
    "title": "User",
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 1,
            "maxLength": 150
        },
        "password": {
            "type": "string",
            "minLength": 8,
            "maxLength": 128
        }
    }
}
