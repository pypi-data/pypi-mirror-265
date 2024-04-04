# SPDX-FileCopyrightText: 2024-present Trenton H <rda0128ou@mozmail.com>
#
# SPDX-License-Identifier: MPL-2.0
from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING
from typing import Generator

from simpleiso3166._compat import slots_dataclass_decorator
from simpleiso3166.subdivisions import Subdivision

if TYPE_CHECKING:
    from simpleiso3166.countries.types import CountryCodeAlpha2Type
    from simpleiso3166.subdivisions.types import SubdivisionCodeType


@slots_dataclass_decorator
class Country:
    """
    Data object containing information about a single country.

    Subdivisions are accessible via the ``subdivisions`` attribute, which loads lazily.
    """

    alpha2: CountryCodeAlpha2Type
    name: str
    common_name: str | None
    _actual_subdivisions: dict[str, Subdivision] = field(init=False, default_factory=dict, repr=False)
    _subdivisions_loaded: bool = field(init=False, default=False, repr=False)

    def _check_and_load(self) -> None:
        """
        If not already loaded, loads the subdivisions for this country
        """
        if not self._subdivisions_loaded:
            for sub in Subdivision.from_country_alpha2(self.alpha2):
                self._actual_subdivisions[sub.code] = sub
            self._subdivisions_loaded = True

    def contains_subdivision(self, subdivision_code: str) -> bool:
        """
        Returns True if the given subdivision code is a valid subdivision of this country
        """
        self._check_and_load()
        return subdivision_code in self._actual_subdivisions

    @property
    def subdivisions(self) -> Generator[Subdivision, None, None]:
        """
        Iterator over all subdivisions of this country
        """
        self._check_and_load()
        for sub in self._actual_subdivisions:
            yield self._actual_subdivisions[sub]

    def get_subdivision(self, subdivision_code: SubdivisionCodeType) -> Subdivision | None:
        """
        Returns the subdivision with the given code if it exists, otherwise returns None.

        See also contains_subdivision for a more convenient way to check if the given code is valid.
        """
        self._check_and_load()
        return self._actual_subdivisions.get(subdivision_code)

    def get_subdivision_name(self, subdivision_code: SubdivisionCodeType) -> str | None:
        """
        Accessor to convert a subdivision code to its name, or None if the given code is not valid for this country.
        """
        self._check_and_load()
        subdivision = self.get_subdivision(subdivision_code)
        if subdivision:
            return subdivision.name
        return None

    @staticmethod
    def from_alpha2(alpha2: CountryCodeAlpha2Type) -> Country | None:
        """
        Constructs a Country object from an alpha-2 code, if the code is valid.
        """
        from simpleiso3166.countries.data import ALPHA2_CODE_TO_COUNTRIES

        return ALPHA2_CODE_TO_COUNTRIES.get(alpha2)

    @staticmethod
    def from_exact_name(name: str) -> Country | None:
        """
        Constructs a Country object from an exact name, if the name is valid.
        """
        from simpleiso3166.countries.data import ALPHA2_CODE_TO_COUNTRIES

        for country in ALPHA2_CODE_TO_COUNTRIES.values():
            if country.name == name:
                return country
        return None

    @staticmethod
    def from_partial_name(country_name: str, *, ratio: float | int = 75.0) -> Generator[Country, None, None]:
        """
        Attempts to locate a country by partial name, using the given ratio of similarity to the given name.

        The results are returned with the most similar first.

        The comparsision is using token_set_ratio from RapidFuzz.

        This is a good starting point, but it needs improvement.  Aliases in particular need to be handled in some way
        """
        # TODO: This needs improvement.  Aliases, better methods, you name it
        from rapidfuzz.fuzz import token_set_ratio
        from rapidfuzz.utils import default_process

        from simpleiso3166.aliases import COUNTRY_ALIAS_TO_CODE
        from simpleiso3166.countries.data import ALPHA2_CODE_TO_COUNTRIES

        processed_name = default_process(country_name)

        results: list[tuple[float, Country]] = []

        for country_code in ALPHA2_CODE_TO_COUNTRIES:
            country = ALPHA2_CODE_TO_COUNTRIES[country_code]
            for name_field in [country.name, country.common_name]:
                if name_field is not None:
                    similarity = token_set_ratio(processed_name, default_process(name_field))
                    if similarity >= ratio:
                        results.append((similarity, country))
                        break
        for alias in COUNTRY_ALIAS_TO_CODE:
            similarity = token_set_ratio(processed_name, default_process(alias))
            if similarity >= ratio:
                results.append((similarity, ALPHA2_CODE_TO_COUNTRIES[COUNTRY_ALIAS_TO_CODE[alias]]))

        sent = set()

        for result in sorted(results, key=lambda x: x[0], reverse=True):  # type: ignore[misc]
            if result[1].alpha2 not in sent:
                yield result[1]
                sent.add(result[1].alpha2)

    @staticmethod
    def is_valid_code(code: str) -> bool:
        from simpleiso3166.countries.data import ALPHA2_CODE_TO_COUNTRIES

        return code in ALPHA2_CODE_TO_COUNTRIES
