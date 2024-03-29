from netsome import constants as c
from netsome.validators import bgp as validators


class ASN:
    def __init__(self, number: int) -> None:
        validators.validate_asplain(number)
        self._number = number

    def to_asdot(self):
        integer, remainder = divmod(self._number, c.TWO_BYTES)
