CREATE_SCHEMA = {
    "title": "Admin",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        },
        "phone_number": {
            "type": ["string", "null"],
            "pattern": "^[+]?[(]?[0-9]{1,4}[)]?[-s./0-9]*$",
            "minLength": 7,
            "maxLength": 20
        },
        "email": {
            "type": "string",
            "format": "email"
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
        "email",
        "gym_id",
        "address_city",
        "address_street"
    ]
}

UPDATE_SCHEMA = {
    "title": "Admin",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        },
        "phone_number": {
            "type": ["string", "null"],
            "pattern": "^[+]?[(]?[0-9]{1,4}[)]?[-s./0-9]*$",
            "minLength": 7,
            "maxLength": 20
        },
        "email": {
            "type": "string",
            "format": "email"
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
