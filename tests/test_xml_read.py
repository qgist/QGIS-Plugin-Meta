# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    tests/test_xml_read.py: Read & parse metadata XML files

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

from .lib import get_xmls, get_xml_items

from qgspluginmeta import import_xml, QgsMetadata

import pytest

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TEST(s)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@pytest.mark.parametrize("qgis_version,xml_item", get_xml_items())
def test_xml_item_read(qgis_version, xml_item):

    release1 = QgsMetadata.from_xmldict(xml_item)

    assert repr(release1).startswith("<QgsMetadata ")

    release2 = QgsMetadata.from_xmldict(release1.as_xmldict())

    assert repr(release2).startswith("<QgsMetadata ")


@pytest.mark.parametrize("qgis_version,xml", get_xmls())
def test_xml_read(qgis_version, xml):

    releases = import_xml(xml)

    assert all((isinstance(release, QgsMetadata) for release in releases))
