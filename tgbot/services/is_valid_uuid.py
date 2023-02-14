import uuid


def is_valid_uuid(value) -> bool:
    """
    Check if a string is a valid UUID version 4.

    :param value: he string to be checked.
    :return: True if the string is a valid UUID version 4, False otherwise.
    """
    try:
        uuid.UUID(value, version=4)
        return True
    except ValueError:
        return False
