CREATE_SCHEMA = {
    "title": "Member",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "maxLength": 255
        },
        "birth_date": {
            "type": "string",
            "format": "date",
            "pattern": "^(19|20)\\d\\d-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
        },
        "phone_number": {
            "type": "string",
            "pattern": "^[+]?[(]?[0-9]{1,4}[)]?[-s./0-9]*$",
            "minLength": 7,
            "maxLength": 20,
        }
    },
    "required": [
        "name",
        "birth_date"
    ]
}

UPDATE_SCHEMA = {
    "title": "Member",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "maxLength": 255
        },
        "birth_date": {
            "type": "string",
            "format": "date",
            "pattern": "^(19|20)\\d\\d-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
        },
        "phone_number": {
            "type": "string",
            "pattern": "^[+]?[(]?[0-9]{1,4}[)]?[-s./0-9]*$",
            "minLength": 7,
            "maxLength": 20,
        }
    }
}
