CREATE_SCHEMA = {
    "title": "HallMachine",
    "type": "object",
    "properties": {
        "hall_id": {
            "type": "integer"
        },
        "machine_id": {
            "type": "integer"
        },
        "name": {
            "type": "string",
            "maxLength": 255
        },
        "uid": {
            "type": "string",
            "maxLength": 100
        }
    },
    "required": [
        "hall_id",
        "machine_id"
    ]
}

UPDATE_SCHEMA = {
    "title": "HallMachine",
    "type": "object",
    "properties": {
        "hall_id": {
            "type": "integer"
        },
        "machine_id": {
            "type": "integer"
        },
        "name": {
            "type": "string",
            "maxLength": 255
        },
        "uid": {
            "type": "string",
            "maxLength": 100
        }
    }
}
