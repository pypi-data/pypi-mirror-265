import appstream_python
from lxml import etree
import pytest_subtests
import requests_mock
import datetime
import pathlib


DATA_DIR = pathlib.Path(__file__).parent / "data"


def _assert_release_list(release_list: appstream_python.ReleaseList) -> None:
    assert len(release_list) == 4

    assert release_list[0].version == "0.4.5"
    assert release_list[0].type == "stable"
    assert release_list[0].urgency == "unknown"
    assert release_list[0].date == datetime.date.fromisoformat("2022-08-20")
    assert release_list[0].date_eol is None
    assert release_list[0].description.items[1].content.get_default_list()[0] == "Display device name for camera ID on Linux"

    assert release_list[1].version == "0.4.4"
    assert release_list[1].type == "development"
    assert release_list[1].urgency == "unknown"
    assert release_list[1].date == datetime.date.fromisoformat("2021-12-16")
    assert release_list[1].date_eol is None
    assert release_list[1].description.items[1].content.get_default_list()[0] == "Implement z-stack capture feature for Miniscopes with an EWL"

    assert release_list[2].version == "0.4.3"
    assert release_list[2].type == "stable"
    assert release_list[2].urgency == "high"
    assert release_list[2].date is None
    assert release_list[2].date_eol is None
    assert release_list[2].description.items[1].content.get_default_list()[0] == "Make build instructions a bit more beginner-friendly"

    assert release_list[3].version == "0.4.2"
    assert release_list[3].type == "stable"
    assert release_list[3].urgency == "unknown"
    assert release_list[3].date == datetime.date.fromisoformat("2021-05-24")
    assert release_list[3].date_eol == datetime.date.fromisoformat("2023-10-24")
    assert release_list[3].description.items[1].content.get_default_list()[0] == "Add spin boxes for sliding values, in addition to slider widgets"


def test_external_releases_component(requests_mock: requests_mock.Mocker) -> None:
    component = appstream_python.AppstreamComponent.from_file(DATA_DIR / "AppStream" / "org.external.releases.xml")

    assert component.releases.type == "external"
    assert len(component.releases) == 0

    requests_mock.get("https://example.org/releases.xml", text=(DATA_DIR / "Releases" / "ReleaseTest.xml").read_text(encoding="utf-8"))

    component.releases.load_external_releases()

    _assert_release_list(component.releases)


def test_load_releases_tag(subtests: pytest_subtests.SubTests, requests_mock: requests_mock.Mocker) -> None:
    tag = etree.fromstring((DATA_DIR / "AppStream" / "org.external.releases.xml").read_bytes()).find("releases")

    with subtests.test("Default"):
        assert len(appstream_python.ReleaseList.from_tag(tag)) == 0

    with subtests.test("Fetch External"):
        requests_mock.get("https://example.org/releases.xml", text=(DATA_DIR / "Releases" / "ReleaseTest.xml").read_text(encoding="utf-8"))
        _assert_release_list(appstream_python.ReleaseList.from_tag(tag, fetch_external=True))


def test_load_releases_file() -> None:
    _assert_release_list(appstream_python.ReleaseList.from_file(DATA_DIR / "Releases" / "ReleaseTest.xml"))


def test_load_releases_url(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get("https://example.org/releases.xml", text=(DATA_DIR / "Releases" / "ReleaseTest.xml").read_text(encoding="utf-8"))

    _assert_release_list(appstream_python.ReleaseList.from_url("https://example.org/releases.xml"))


def test_write_and_read_releases_file(tmp_path: pathlib.Path) -> None:
    releases_list = appstream_python.ReleaseList.from_file(DATA_DIR / "Releases" / "ReleaseTest.xml")

    releases_list.save_file(tmp_path / "releases.xml")

    assert releases_list == appstream_python.ReleaseList.from_file(tmp_path / "releases.xml")
