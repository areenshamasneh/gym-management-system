CREATE_SCHEMA = {
    "title": "Machine",
    "type": "object",
    "properties": {
        "serial_number": {
            "type": "string",
            "maxLength": 100
        },
        "type": {
            "type": "string",
            "enum": [
                "walking",
                "running",
                "cycling",
                "elliptical",
                "rowing",
                "stair_climber"
            ]
        },
        "model": {
            "type": "string",
            "maxLength": 100
        },
        "brand": {
            "type": "string",
            "maxLength": 100
        },
        "status": {
            "type": "string",
            "enum": [
                "operational",
                "broken"
            ]
        },
        "maintenance_date": {
            "type": "string",
            "format": "date"
        }
    },
    "required": [
        "serial_number",
        "type",
        "status"
    ]
}

UPDATE_SCHEMA = {
    "title": "Machine",
    "type": "object",
    "properties": {
        "serial_number": {
            "type": "string",
            "maxLength": 100
        },
        "type": {
            "type": "string",
            "enum": [
                "walking",
                "running",
                "cycling",
                "elliptical",
                "rowing",
                "stair_climber"
            ]
        },
        "model": {
            "type": "string",
            "maxLength": 100
        },
        "brand": {
            "type": "string",
            "maxLength": 100
        },
        "status": {
            "type": "string",
            "enum": [
                "operational",
                "broken"
            ]
        },
        "maintenance_date": {
            "type": "string",
            "format": "date"
        }
    }
}
