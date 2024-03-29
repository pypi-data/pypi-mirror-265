from netsome import constants as c


def validate_asplain(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError("Invalid asplain type, must be int")

    if number < c.ZERO or number > c.ASN_MAX:
        raise ValueError(
            f"Invalid asplain number. Must be in range {c.ZERO}-{c.ASN_MAX}"
        )


def validate_asdotplus(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid asdot type, must be str")

    if c.DOT not in string:
        raise ValueError("Invalid asdot+ format, must be high.low")

    integer, remainder = map(int, string.split(c.DOT, maxsplit=1))
    validate_asplain(integer * c.TWO_BYTES + remainder)


def validate_asdot(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid asdot type, must be str")

    if c.DOT in string:
        validate_asdotplus(string)
        return

    validate_asplain(int(string))
