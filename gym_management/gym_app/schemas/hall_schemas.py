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
        "hall_type_id": {
            "type": "integer"
        },
        "gym_id": {
            "type": "string",
            "minimum": 1
        }
    },
    "required": [
        "name",
        "users_capacity",
        "hall_type_id",
        "gym_id"
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
        "hall_type_id": {
            "type": "integer"
        },
        "gym_id": {
            "type": "string",
            "minimum": 1
        }
    }
}
