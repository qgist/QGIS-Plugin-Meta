# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    src/qgspluginmeta/_core/repo.py: Import / export of entire XML files for repos

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

import typing

from .abc import QgsMetadataABC
from .metadata import QgsMetadata

from typeguard import typechecked
import xmltodict

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@typechecked
def import_xml(xml_string: str) -> typing.List[QgsMetadataABC]:
    """
    Expects a (UTF-8) string containing an entire XML document (`plugins.xml`)
    """

    xml_string = xml_string.replace('& ', '&amp; ') # From plugin installer: Fix lonely ampersands in metadata
    tree = xmltodict.parse(xml_string)

    if isinstance(tree['plugins']['pyqgis_plugin'], list): # more than one
        return [QgsMetadata.from_xmldict(release_dict) for release_dict in tree['plugins']['pyqgis_plugin']]
    return [QgsMetadata.from_xmldict(tree['plugins']['pyqgis_plugin'])] # just one


@typechecked
def export_xml(metadata: typing.List[QgsMetadataABC]) -> str:

    return xmltodict.unparse({'plugins': {'pyqgis_plugin': [
        metaobject.as_xmldict() for metaobject in metadata
    ]}}, pretty=True)
