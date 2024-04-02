from typing import Optional


def camel2snake(title: str) -> str:
    """
    Converts a camelCase string to a snake_case string.

    Parameters:
        title (str): The camelCase string to be converted.

    Returns:
        str: The converted snake_case string.

    Examples:
        >>> camel2snake("camelCaseExample")
        'camel_case_example'
        >>> camel2snake("CamelCaseExample")
        'camel_case_example'
    """
    new_title = ""
    underscore = False
    for letter in title:
        if 65 <= ord(letter) <= 90:
            if underscore:
                new_title += '_'
                underscore = False
            new_title += chr(ord(letter) + 32)
        else:
            underscore = True
            new_title += letter
    return new_title


def snake2camel(title: str, exceptions: Optional[tuple[str]] = None) -> str:
    """
    Converts a snake_case string to a camelCase string, with optional exceptions
    where the conversion should not be applied.

    Parameters:
        title (str): The snake_case string to be converted.
        exceptions (Optional[tuple[str]]): A tuple of strings that, when matched at the
                                      beginning of the title, prevent conversion and
                                      return the title as is. Defaults to None.

    Returns:
        str: The converted camelCase string if no exception is matched; otherwise,
             the original string.

    Examples:
        >>> snake2camel("snake_case_example")
        'snakeCaseExample'
        >>> snake2camel("id_example", exceptions=("id_",))
        'id_example'

    Notes:
        - The first segment of the snake_case string remains lowercase, aligning
          with the camelCase convention.
        - If the title starts with any of the specified exceptions, it is returned
          unchanged, useful for preserving certain identifiers.
    """
    if exceptions is None:
        exceptions = ("id_",)
    if title.startswith(exceptions):
        return title
    title_list = title.split('_')
    title_list = [title_list[0]] + [word[0].upper() + word[1:] for word in title_list][1:]
    return ''.join(title_list)
