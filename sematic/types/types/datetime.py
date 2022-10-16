# Standard Library
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Datetime:
    """
      Datetime lets user display native python object in the UI with specified
        formating

      Parameters
      ----------
      datetime_value: datetime
          The datetime python object
      label: str
          The label of the datetime
      display_format: str
          Format of the date and time in the UI.
          See https://date-fns.org/v2.25.0/docs/format for more format information.

    Raises
    ------
    ValueError
        no display_format is specified
    """

    iso_string: str
    label: str
    display_format: str

    def __init__(
        self,
        datetime_value: datetime,
        label: str,
        display_format: str = "MM/dd/yyyy HH:mm",
    ):
        if display_format == "":
            raise ValueError("No date time display format specified")
        self.iso_string = datetime_value.isoformat()
        self.label = label
        self.display_format = display_format
