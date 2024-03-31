import appstream_python
from lxml import etree
import pathlib


DATA_DIR = pathlib.Path(__file__).parent / "data" / "AppStream"
JDTEXTEDIT_METAINFO = DATA_DIR / "com.gitlab.JakobDev.jdTextEdit.metainfo.xml"


def assert_component_jdtextedit(component: appstream_python.AppstreamComponent) -> None:
    assert component.id == "com.gitlab.JakobDev.jdTextEdit"
    assert component.name.get_default_text() == "jdTextEdit"
    assert component.summary.get_default_text() == "An advanced text editor"
    assert component.developer.name.get_default_text() == "JakobDev"
    assert component.developer.id is None
    assert component.project_license == "GPL-3.0-only"
    assert component.metadata_license == "CC0-1.0"
    assert component.project_group is None

    assert len(component.launchables) == 1
    assert component.launchables["desktop-id"] == "com.gitlab.JakobDev.jdTextEdit.desktop"

    assert len(component.urls) == 4
    assert component.urls["homepage"] == "https://gitlab.com/JakobDev/jdTextEdit"
    assert component.urls["bugtracker"] == "https://gitlab.com/JakobDev/jdTextEdit/-/issues"
    assert component.urls["help"] == "https://jdtextedit.readthedocs.io"
    assert component.urls["vcs-browser"] == "https://gitlab.com/JakobDev/jdTextEdit"

    assert len(component.releases) == 25
    assert component.releases.type == "embedded"
    assert component.releases[0].version == "10.3"

    assert component.display_length["recommends"][0].px == 760
    assert component.display_length["recommends"][0].compare == "ge"


def test_from_component_tag() -> None:
    root = etree.parse(JDTEXTEDIT_METAINFO)
    component = appstream_python.AppstreamComponent.from_component_tag(root)
    assert_component_jdtextedit(component)


def test_from_file() -> None:
    component = appstream_python.AppstreamComponent.from_file(JDTEXTEDIT_METAINFO)
    assert_component_jdtextedit(component)


def test_from_bytes() -> None:
    with open(JDTEXTEDIT_METAINFO, "rb") as f:
        component = appstream_python.AppstreamComponent.from_bytes(f.read())
    assert_component_jdtextedit(component)


def test_from_string() -> None:
    with open(JDTEXTEDIT_METAINFO, "r") as f:
        component = appstream_python.AppstreamComponent.from_string(f.read())
    assert_component_jdtextedit(component)


def test_save_jdtextedit_data(tmp_path: pathlib.Path) -> None:
    old_component = appstream_python.AppstreamComponent.from_file(JDTEXTEDIT_METAINFO)
    old_component.save_file(tmp_path / "jdTextEdit.metainfo.xml")

    new_component = appstream_python.AppstreamComponent.from_file(tmp_path / "jdTextEdit.metainfo.xml")
    assert_component_jdtextedit(new_component)


def test_data_appstream_cli() -> None:
    component = appstream_python.AppstreamComponent.from_file(DATA_DIR / "org.freedesktop.appstream.cli.metainfo.xml")

    assert component.project_group == "Freedesktop"
    assert component.developer.id == "org.freedesktop"
    assert component.developer.name.get_default_text() == "Matthias Klumpp"
