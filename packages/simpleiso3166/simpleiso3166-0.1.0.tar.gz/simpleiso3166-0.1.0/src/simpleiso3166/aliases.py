# SPDX-FileCopyrightText: 2024-present Trenton H <rda0128ou@mozmail.com>
#
# SPDX-License-Identifier: MPL-2.0
from typing import Final

from simpleiso3166.countries.types import CountryCodeAlpha2Type
from simpleiso3166.subdivisions.types import SubdivisionCodeType

COUNTRY_ALIAS_TO_CODE: Final[dict[str, CountryCodeAlpha2Type]] = {
    "England": "GB",  # United Kingdom
    "Great Britain": "GB",  # United Kingdom
    "America": "US",  # United States of America
    "USA": "US",  # United States of America
    "Korea": "KR",  # Republic of Korea
    "Republic of Korea": "KR",  # Republic of Korea
    "Holland": "NL",  # Kingdom of the Netherlands
}

SUBDIVISION_ALIAS_TO_CODE: Final[dict[str, SubdivisionCodeType]] = {}
