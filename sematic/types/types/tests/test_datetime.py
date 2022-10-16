# Third-party
# Standard Library
from datetime import datetime

import pytest

# Sematic
from sematic.types.types.datetime import Datetime


def test_datetime_iso_string_valid():
    now = datetime.now()
    display_format = "MM/dd/yyyy HH:mm"
    label = "Default datetime format"
    datetime_component = Datetime(now, label, display_format)
    assert datetime_component.label == label
    assert datetime_component.display_format == display_format
    assert datetime_component.iso_string == now.isoformat()


@pytest.mark.parametrize(
    "expected_exception_str, display_format",
    (("No date time display format specified", ""),),
)
def test_url_validation_fail(expected_exception_str, display_format):
    # with pytest.raises(ValueError, match=expected_exception_str):
    with pytest.raises(ValueError, match=expected_exception_str):
        Datetime(datetime.now(), label="test label", display_format=display_format)
