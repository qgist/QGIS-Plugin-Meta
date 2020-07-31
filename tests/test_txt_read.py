# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    tests/test_txt_read.py: Read & parse metadata txt files

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

from .lib import get_txts

from qgspluginmeta import QgsBoolValueError, QgsPluginMetadata, QgsVersion

import pytest

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TEST(s)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@pytest.mark.parametrize("plugin_id,plugin_version,txt", get_txts())
def test_txt_read(plugin_id, plugin_version, txt):

    if (plugin_id, plugin_version) in (
        ("geometry_paster", "0.1.1"),
        ("pandora", "2.0.1"),
        ("qgis-select-by-radius-plus-plugin", "0.1"),
        ("qgis-select-by-radius-plus-plugin", "0.3"),
    ):
        with pytest.raises(QgsBoolValueError):
            meta = QgsPluginMetadata.from_metadatatxt(plugin_id, txt)
        return

    meta1 = QgsPluginMetadata.from_metadatatxt(plugin_id, txt)

    assert repr(meta1) == f'<QgsPluginMetadata id="{plugin_id:s}">'

    if meta1['qgisMinimumVersion'].value >= QgsVersion.from_qgisversion('3.0.0'):
        assert meta1.required_fields_present()
    elif meta1['qgisMaximumVersion'].value_set:
        if meta1['qgisMaximumVersion'].value > QgsVersion.from_qgisversion('3.0.0'):
            assert meta1.required_fields_present()

    meta2 = QgsPluginMetadata.from_metadatatxt(plugin_id, meta1.as_metadatatxt())

    assert repr(meta2) == f'<QgsPluginMetadata id="{plugin_id:s}">'

    if meta2['qgisMinimumVersion'].value >= QgsVersion.from_qgisversion('3.0.0'):
        assert meta2.required_fields_present()
    elif meta2['qgisMaximumVersion'].value_set:
        if meta2['qgisMaximumVersion'].value > QgsVersion.from_qgisversion('3.0.0'):
            assert meta2.required_fields_present()
