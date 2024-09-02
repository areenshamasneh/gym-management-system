CREATE_SCHEMA = {
    "title": "Hall",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "maxLength": 255
        },
        "users_capacity": {
            "type": "integer",
            "minimum": 1
        },
        "hall_type": {
            "type": "integer"
        }
    },
    "required": [
        "name",
        "users_capacity",
        "hall_type"
    ]
}

UPDATE_SCHEMA = {
    "title": "Hall",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "maxLength": 255
        },
        "users_capacity": {
            "type": "integer",
            "minimum": 1
        },
        "hall_type": {
            "type": "integer"
        }
    }
}
