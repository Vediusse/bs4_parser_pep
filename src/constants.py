from pathlib import Path

MAIN_DOC_URL = "https://docs.python.org/3/"

PEP_DOC_URL = "https://peps.python.org/"
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

display_format = ("pretty", "file")

EXPECTED_STATUS = {
    "A": ("Active", "Accepted"),
    "D": ("Deferred",),
    "F": ("Final",),
    "P": ("Provisional",),
    "R": ("Rejected",),
    "S": ("Superseded",),
    "W": ("Withdrawn",),
    "": ("Draft", "Active"),
}

AMOUNT_STATUS = {
    "A": 0,
    "D": 0,
    "F": 0,
    "P": 0,
    "R": 0,
    "S": 0,
    "W": 0,
    "": 0,
}
