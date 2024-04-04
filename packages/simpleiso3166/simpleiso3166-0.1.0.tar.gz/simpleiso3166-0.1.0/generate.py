import json
import sys
from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path

from rich.progress import track

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired
    from typing_extensions import TypedDict

else:
    from typing import NotRequired
    from typing import TypedDict


from httpx import Client

ISO_3166_1_JSON_URL = "https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main/data/iso_3166-1.json?ref=d055275324963c9bce5882eaaa93024cf2bf7ed0"
ISO_3166_2_JSON_URL = "https://salsa.debian.org/iso-codes-team/iso-codes/-/raw/main/data/iso_3166-2.json?ref=4f5658fa63afce8cd121d41444b28c2294e6b513"


class Iso3116TypeOneEntry(TypedDict):
    alpha_2: str
    alpha_3: str
    flag: str
    common_name: NotRequired[str]
    official_name: NotRequired[str]
    name: NotRequired[str]
    numeric: NotRequired[str]


class Iso3116TypeTwoEntry(TypedDict):
    code: str
    name: str
    type: str


class CombinedData(TypedDict):
    name: str
    common_name: str | None
    alpha_2: str
    subdivisions: list[Iso3116TypeTwoEntry]


def common_header(f: TextIOWrapper, revision: str) -> None:
    f.writelines(
        [
            "# SPDX-FileCopyrightText: 2024-present Trenton H <rda0128ou@mozmail.com>\n",
            "#\n",
            "# SPDX-License-Identifier: MPL-2.0\n",
            f"# Generated from: {revision}\n",
        ],
    )


def get_country_comment_name(country_data: CombinedData) -> str:
    if country_data["common_name"] is not None:
        return country_data["common_name"]
    else:
        assert country_data["name"] is not None  # noqa: S101
        return country_data["name"]


def output_country_data(
    module_dir: Path,
    combined_data: dict[str, CombinedData],
    revision: str = "d055275324963c9bce5882eaaa93024cf2bf7ed0",
):

    countries_dir = module_dir / "countries"
    country_mapping_file = countries_dir / "data.py"
    country_type_file = countries_dir / "types.py"

    if not countries_dir.exists():
        countries_dir.mkdir(parents=True, exist_ok=True)

    with country_type_file.open("w", encoding="utf-8", newline="\n") as f:
        common_header(f, revision)
        f.write("from typing import Literal\n\n")
        f.write("CountryCodeAlpha2Type = Literal[\n")
        for country_code in track(sorted(combined_data), description="Writing country codes...     "):
            comment_name = get_country_comment_name(combined_data[country_code])
            f.write(
                f'    "{combined_data[country_code]["alpha_2"]}",  # {comment_name}\n',
            )
        f.write("]\n")

    with country_mapping_file.open("w", encoding="utf-8", newline="\n") as f:
        common_header(f, revision)
        f.writelines(
            [
                "from typing import Final\n\n"
                "from simpleiso3166.countries import Country\n"
                "from simpleiso3166.countries.types import CountryCodeAlpha2Type\n\n",
            ],
        )

        for country_code in track(sorted(combined_data), description="Writing country data...      "):
            f.write(f"{country_code}: Final[Country] = ")
            f.write(f'Country("{country_code}",')
            for key in ["name", "common_name"]:
                if combined_data[country_code][key] is None:
                    f.write(" None")
                else:
                    f.write(f' "{combined_data[country_code][key]}"')
                if key != "common_name":
                    f.write(",")
            f.write(")\n")
        f.write("\n")

        f.write("ALPHA2_CODE_TO_COUNTRIES: Final[dict[CountryCodeAlpha2Type, Country]] = {\n")
        for country_code in combined_data:
            f.write(f'    "{country_code}": {country_code},\n')
        f.write("}\n")


def output_subdivision_data(
    module_dir: Path,
    combined_data: dict[str, CombinedData],
    revision: str = "4f5658fa63afce8cd121d41444b28c2294e6b513",
):
    subdivision_dir = module_dir / "subdivisions"
    subdivision_data_dir = subdivision_dir / "data"
    subdivision_type_file = subdivision_dir / "types.py"

    if not subdivision_dir.exists():
        subdivision_dir.mkdir(parents=True, exist_ok=True)

    if not subdivision_data_dir.exists():
        subdivision_data_dir.mkdir(parents=True, exist_ok=True)

    with subdivision_type_file.open("w", encoding="utf-8", newline="\n") as f:
        f.write("from typing import Literal\n\n")
        f.write("SubdivisionCodeType = Literal[\n")
        for country_code in track(sorted(combined_data), description="Writing subdivisions types..."):
            country = combined_data[country_code]
            country_name = country["name"]
            f.write(f"    # {country_name}\n")
            if not country["subdivisions"]:
                f.write("    # (no subdivisions)\n")
            for subdivision in country["subdivisions"]:
                subdivision_code: str = subdivision["code"]
                name: str = subdivision["name"]
                f.write(f'    "{subdivision_code}",  # {name}\n')
        f.write("]\n\n")

    for country_code in track(sorted(combined_data), description="Writing subdivisions...      "):
        country = combined_data[country_code]
        with (subdivision_data_dir / f"{country_code.upper()}.py").open("w", encoding="utf-8", newline="\n") as f:
            common_header(f, revision)
            f.writelines(
                [
                    "from typing import Final\n\n",
                    "from simpleiso3166.subdivisions import Subdivision\n\n",
                ],
            )
            country_name = country["name"]
            f.write(f'COUNTRY_NAME: Final[str] = "{country_name}"\n\n')
            f.write("SUBDIVISIONS: Final[list[Subdivision]] = [\n")
            for subdivision in country["subdivisions"]:
                name: str = subdivision["name"]
                code = subdivision["code"]
                f.write(f'    Subdivision("{code}", "{name}"),\n')
            f.write("]\n")


def main(
    data_dir: Path = Path(),
    module_dir: Path = Path("src") / "simpleiso3166",
    *,
    force_update: bool = False,
):
    country_json = data_dir / "iso_3166-1.json"
    subdivision_json = data_dir / "iso_3166-2.json"
    for output_file, url in zip(
        [country_json, subdivision_json],
        [ISO_3166_1_JSON_URL, ISO_3166_2_JSON_URL],
        strict=True,
    ):
        if force_update or not output_file.exists():
            with Client() as client:
                response = client.get(url)
                response.raise_for_status()
                output_file.write_bytes(response.content)

    subdivision_data: list[Iso3116TypeTwoEntry] = json.loads(subdivision_json.read_text(encoding="utf-8"))["3166-2"]
    country_data: list[Iso3116TypeOneEntry] = json.loads(country_json.read_text(encoding="utf-8"))["3166-1"]

    if not module_dir.exists():
        module_dir.mkdir(parents=True, exist_ok=True)

    country_code_to_subdivision: dict[str, list] = defaultdict(list)

    for subdivision in subdivision_data:
        subdivision_code: str = subdivision["code"]
        country_alpha_2 = subdivision_code.split("-")[0]
        country_code_to_subdivision[country_alpha_2].append(subdivision)

    combined_data: dict[str, CombinedData] = {}

    for country in track(country_data, description="Combining data...            "):
        common_name = country.get("common_name")
        official_name = country.get("official_name")
        name = country.get("name")

        used_name = None

        if official_name:
            used_name = official_name
        elif name:
            used_name = name
        assert used_name is not None  # noqa: S101
        assert isinstance(used_name, str)  # noqa: S101

        if not common_name and used_name == official_name:
            common_name = name

        if used_name.lower().endswith("of"):
            used_name = " ".join(used_name.split(",", maxsplit=1)[::-1]).strip()

        country_alpha_2 = country["alpha_2"]
        combined_data[country_alpha_2] = {
            "alpha_2": country_alpha_2,
            "name": used_name,
            "common_name": common_name,
            "subdivisions": country_code_to_subdivision.get(country_alpha_2, []),
        }

    output_country_data(module_dir, combined_data)

    output_subdivision_data(module_dir, combined_data)


if __name__ == "__main__":
    import typer

    typer.run(main)
