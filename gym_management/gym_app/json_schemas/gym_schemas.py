CREATE_SCHEMA = {
    "title": "Gym",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        },
        "type": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "description": {
            "type": ["string", "null"],
            "maxLength": 500
        },
        "address_city": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        },
        "address_street": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        }
    },
    "required": [
        "name",
        "type",
        "address_city",
        "address_street"
    ]
}

UPDATE_SCHEMA = {
    "title": "Gym",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        },
        "type": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "description": {
            "type": ["string", "null"],
            "maxLength": 500
        },
        "address_city": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        },
        "address_street": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        }
    }
}
