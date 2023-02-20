"""

"""
def validate(message: str, content: dict):
    invalid_content = (
        content is None or
        all(key in content for key in ("secret")) is not True
    )

    if invalid_content:
        result = (
            {
                "status": "Failed",
                "message": message
            },
            400
        )
        return (False, result)
    return (True, None)

