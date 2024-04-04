from simpleiso3166.subdivisions import Subdivision


class TestSubdivisionSearch:

    def test_subdivision_search(self) -> None:
        results = list(Subdivision.search_by_name("Connecticut"))

        assert len(results) == 1
        assert results[0].code == "US-CT"

        results = list(Subdivision.search_by_name("Tasmania"))

        assert len(results) == 2
        codes = [x.code for x in results]
        names = [x.name for x in results]

        assert codes == ["AU-TAS", "NZ-TAS"]
        assert names == ["Tasmania", "Tasman"]

    def test_multiple_matches(self) -> None:
        results = list(Subdivision.search_by_name("Saint George"))

        assert len(results) == 7
        codes = [x.code for x in results]
        names = [x.name for x in results]
        assert codes == ["AG-03", "BB-03", "DM-04", "GD-03", "KN-03", "KN-04", "VC-04"]
        assert names == [
            "Saint George",
            "Saint George",
            "Saint George",
            "Saint George",
            "Saint George Basseterre",
            "Saint George Gingerland",
            "Saint George",
        ]
