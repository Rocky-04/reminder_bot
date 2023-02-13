import datetime


async def first_date_filter(text: str) -> bool:
    """
    Check if the input text is a valid date with format '%Y-%m-%d %H:%M'
    and is greater than the current date.

    :param text: The input text to be checked
    :return: True if the text is a valid date in the specified format and is greater
    than the current date, False otherwise.
    """
    try:
        first_date = datetime.datetime.strptime(text, '%Y-%m-%d %H:%M')
        if first_date > datetime.datetime.now():
            return True
        else:
            return False
    except ValueError:
        return False


async def name_filter(name: str):
    """
    Check if the input text is a string with length less than or equal to 250.

    :param name: The input name to be checked
    :return: True if the text is a string with length less than or equal to 250, False otherwise.
    """
    if isinstance(name, str) and len(name) <= 250:
        return True
    else:
        return False


async def description_filter(description: str):
    """
    Check if the input description is a string with length less than or equal to 1000.

    :param description: The input description to be checked
    :return: True if the description is a string with length less than or equal to 1000, False otherwise.
    """
    if isinstance(description, str) and len(description) <= 1000:
        return True
    else:
        return False