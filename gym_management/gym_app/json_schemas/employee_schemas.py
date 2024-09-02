CREATE_SCHEMA = {
    "title": "Employee",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        },
        "manager": {
            "type": "integer",
            "nullable": True
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
        },
        "phone_number": {
            "type": ["string", "null"],
            "pattern": "^[+]?[(]?[0-9]{1,4}[)]?[-s./0-9]*$",
            "minLength": 7,
            "maxLength": 20,
            "nullable": True
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "positions": {
            "type": "string",
            "pattern": "^(cleaner|trainer|system_worker)(,(cleaner|trainer|system_worker))*$"
        }
    },
    "required": [
        "name",
        "gym",
        "address_city",
        "address_street",
        "email"
    ]
}

UPDATE_SCHEMA = {
    "title": "Employee",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 255
        },
        "manager": {
            "type": "integer",
            "nullable": True
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
        },
        "phone_number": {
            "type": ["string", "null"],
            "pattern": "^[+]?[(]?[0-9]{1,4}[)]?[-s./0-9]*$",
            "minLength": 7,
            "maxLength": 20,
            "nullable": True
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "positions": {
            "type": "string",
            "pattern": "^(cleaner|trainer|system_worker)(,(cleaner|trainer|system_worker))*$"
        }
    }
}
