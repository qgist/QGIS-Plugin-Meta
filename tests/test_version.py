# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    tests/test_version.py: Parsing and comparing versions

    Copyright (C) 2020 QGIST project <info@qgist.org>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU General Public License
Version 2 ("GPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
https://github.com/qgist/QGIS-Plugin-Meta/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import pytest

from qgspluginmeta import QgsVersion, QgsVersionValueError

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TEST(s)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def test_version_len():

    v = QgsVersion.from_pluginversion("1.2-3_4 5")

    assert len(v) == 5


def test_version_repr():

    v = QgsVersion.from_pluginversion("1")

    assert repr(v).startswith("<QgsVersion ")


def test_version_str():

    v = QgsVersion.from_pluginversion("1.2-3_4 5")

    assert str(v) == "1.2.3.4.5"


def test_version_items():

    v = QgsVersion.from_pluginversion("1.2-3_4 5")

    for index in range(1, 6):
        assert v[index - 1] == str(index)

    with pytest.raises(IndexError):
        item = v[5]
    with pytest.raises(IndexError):
        item = v[-1]


def test_version_compare():

    assert QgsVersion.from_pluginversion("1.2") != QgsVersion.from_pluginversion(
        "1.2.3"
    )
    assert not QgsVersion.from_pluginversion("1.2") == QgsVersion.from_pluginversion(
        "1.2.3"
    )

    assert QgsVersion.from_pluginversion("1.2-3_4 5") == QgsVersion.from_pluginversion(
        "1 2 3 4 5"
    )
    assert not QgsVersion.from_pluginversion("1.2") == QgsVersion.from_pluginversion(
        "1.3"
    )

    assert QgsVersion.from_pluginversion("1.3") != QgsVersion.from_pluginversion("1.2")

    assert QgsVersion.from_pluginversion("1.2") <= QgsVersion.from_pluginversion("1.2")
    assert QgsVersion.from_pluginversion("1.2") >= QgsVersion.from_pluginversion("1.2")

    assert QgsVersion.from_pluginversion("1.2") <= QgsVersion.from_pluginversion("1.3")
    assert not QgsVersion.from_pluginversion("1.3") <= QgsVersion.from_pluginversion(
        "1.2"
    )
    assert QgsVersion.from_pluginversion("1.3") >= QgsVersion.from_pluginversion("1.2")
    assert not QgsVersion.from_pluginversion("1.2") >= QgsVersion.from_pluginversion(
        "1.3"
    )

    assert QgsVersion.from_pluginversion("1.3") > QgsVersion.from_pluginversion("1.2")
    assert not QgsVersion.from_pluginversion("1.3") < QgsVersion.from_pluginversion(
        "1.2"
    )
    assert QgsVersion.from_pluginversion("1.2") < QgsVersion.from_pluginversion("1.3")
    assert not QgsVersion.from_pluginversion("1.2") > QgsVersion.from_pluginversion(
        "1.3"
    )

    assert not QgsVersion.from_pluginversion("1.2") > QgsVersion.from_pluginversion(
        "1.2"
    )
    assert not QgsVersion.from_pluginversion("1.2") < QgsVersion.from_pluginversion(
        "1.2"
    )

    assert QgsVersion.from_pluginversion("1.2.4") > QgsVersion.from_pluginversion(
        "1.2.3"
    )
    assert not QgsVersion.from_pluginversion("1.2.4") < QgsVersion.from_pluginversion(
        "1.2.3"
    )

    assert QgsVersion.from_pluginversion("3.2.1") > QgsVersion.from_pluginversion("3.2")
    assert not QgsVersion.from_pluginversion("3.2.1") < QgsVersion.from_pluginversion(
        "3.2"
    )

    assert QgsVersion.from_pluginversion("1.2") > QgsVersion.from_pluginversion(
        "1.2 alpha"
    )
    assert not QgsVersion.from_pluginversion("1.2") < QgsVersion.from_pluginversion(
        "1.2 alpha"
    )


def test_version_original():

    assert QgsVersion.from_pluginversion("1.2-3_4 5").original == "1.2-3_4 5"

    assert (
        QgsVersion.from_qgisversion("3.99.1", fix_plugin_compatibility=True).original
        == "3.99.1"
    )
    assert QgsVersion.from_qgisversion("3.99.1").original == "3.99.1"


def test_version_stable():

    assert QgsVersion.from_pluginversion("1.2").stable
    assert not QgsVersion.from_pluginversion("1.2 BETA").stable
    assert not QgsVersion.from_pluginversion("1.2 rc 3.5").stable
    assert not QgsVersion.from_pluginversion("1.2 rc").stable
    assert QgsVersion.from_pluginversion("rc 1.2").stable


def test_version_prefix():

    assert QgsVersion.from_pluginversion("VER.1.2") == QgsVersion.from_pluginversion(
        "1.2"
    )
    assert QgsVersion.from_pluginversion(
        "VERSION 1.2"
    ) == QgsVersion.from_pluginversion("1.2")


def test_version_qgis():

    assert QgsVersion.from_qgisversion("3.14.1") == QgsVersion.from_qgisversion(
        "3.14.1"
    )
    assert QgsVersion.from_qgisversion("3.99.1") == QgsVersion.from_qgisversion(
        "3.99.1"
    )
    assert QgsVersion.from_qgisversion("4.0.0") == QgsVersion.from_qgisversion(
        "3.99.1", fix_plugin_compatibility=True
    )


def test_version_qgis_broken():

    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_qgisversion("3")
    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_qgisversion("3.")
    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_qgisversion("3..")
    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_qgisversion("..")
    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_qgisversion("3.14.")
    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_qgisversion("3.14")
    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_qgisversion("3.14.x")
    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_qgisversion("3.x.14")


def test_version_empty():

    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_pluginversion("")
    with pytest.raises(QgsVersionValueError):
        v = QgsVersion.from_qgisversion("")
