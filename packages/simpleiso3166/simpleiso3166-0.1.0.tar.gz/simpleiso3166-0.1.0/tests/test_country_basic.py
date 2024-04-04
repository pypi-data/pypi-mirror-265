from simpleiso3166.countries import Country


class TestCountryBasic:

    def test_get_country_from_known_code(self) -> None:
        country = Country.from_alpha2("US")

        assert country is not None
        assert country.name == "United States of America"
        assert country.common_name == "United States"
        assert country.alpha2 == "US"

    def test_get_invalid_code(self) -> None:
        country = Country.from_alpha2("XX")  # type: ignore[arg-type]

        assert country is None

    def test_country_from_name(self) -> None:
        country = Country.from_exact_name("Hashemite Kingdom of Jordan")

        assert country is not None
        assert country.alpha2 == "JO"
        assert country.common_name == "Jordan"
        assert country.name == "Hashemite Kingdom of Jordan"

    def test_invalid_country_from_name(self) -> None:
        country = Country.from_exact_name("Jordanian")

        assert country is None

    def test_code_validation(self) -> None:
        assert Country.is_valid_code("US")
        assert not Country.is_valid_code("XX")

    def test_name_search(self) -> None:
        results = list(Country.from_partial_name("Saudi"))

        assert len(results) == 1
        assert results[0].alpha2 == "SA"
        assert results[0].common_name == "Saudi Arabia"
        assert results[0].name == "Kingdom of Saudi Arabia"

    def test_name_search_ratio(self) -> None:
        results = list(Country.from_partial_name("Jordn"))

        assert len(results) == 1
        assert results[0].alpha2 == "JO"
        assert results[0].name == "Hashemite Kingdom of Jordan"
        assert results[0].common_name == "Jordan"

    def test_name_search_with_official_name(self) -> None:
        results = list(Country.from_partial_name("Hashemite Kingdom"))

        assert len(results) == 1
        assert results[0].alpha2 == "JO"
        assert results[0].name == "Hashemite Kingdom of Jordan"
        assert results[0].common_name == "Jordan"

    def test_search_nultiple_results(self) -> None:
        results = list(Country.from_partial_name("Kingdom"))

        assert len(results) == 17
        assert results[0].alpha2 == "BE"
        assert results[0].name == "Kingdom of Belgium"
        assert results[0].common_name == "Belgium"

        assert results[10].alpha2 == "NL"
        assert results[10].name == "Kingdom of the Netherlands"
        assert results[10].common_name == "Netherlands"

        assert results[16].alpha2 == "TO"
        assert results[16].name == "Kingdom of Tonga"
        assert results[16].common_name == "Tonga"

    def test_alias_search(self) -> None:
        results = list(Country.from_partial_name("Holland"))

        # The second one is Poland
        assert len(results) == 2
        assert results[0].alpha2 == "NL"
        assert results[0].name == "Kingdom of the Netherlands"
        assert results[0].common_name == "Netherlands"


class TestCountrySubdivision:
    def test_country_load_subdivisions(self) -> None:
        country = Country.from_alpha2("US")

        assert country is not None

        subdivisions = list(country.subdivisions)

        assert len(subdivisions) == 57

        code_to_name = {x.code: x.name for x in subdivisions}

        assert "US-CA" in code_to_name
        assert code_to_name["US-CA"] == "California"
        assert "US-NY" in code_to_name
        assert code_to_name["US-NY"] == "New York"

    def test_country_contains_subdivision(self) -> None:
        country = Country.from_alpha2("DE")

        assert country is not None
        assert country.contains_subdivision("DE-BW")
        assert country.contains_subdivision("DE-HH")

    def test_get_subdivision_by_code(self) -> None:

        country = Country.from_alpha2("DE")

        assert country is not None
        subdivision = country.get_subdivision("DE-BW")

        assert subdivision is not None
        assert subdivision.code == "DE-BW"
        assert subdivision.name == "Baden-Württemberg"

    def test_get_subdivision_name(self) -> None:
        country = Country.from_alpha2("TD")

        assert country is not None

        subdivision = country.get_subdivision_name("TD-KA")
        assert subdivision is not None
        assert subdivision == "Kanem"

        subdivision = country.get_subdivision_name("TD-XX")  # type: ignore[arg-type]
        assert subdivision is None

    def test_double_subdivisions_load(self) -> None:
        for _ in range(2):
            country = Country.from_alpha2("US")

            assert country is not None

            subdivisions = list(country.subdivisions)

            assert len(subdivisions) == 57

            del country
