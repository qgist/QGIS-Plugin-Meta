# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    src/qgspluginmeta/_core/spec.py: Meta data specification

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

from .lib import bool_to_str, str_to_bool
from .version import QgsVersion

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PLUGIN META
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

SPEC = (
    {
        "comment": "module name",
        "dtype": str,
        "name": "id",
        "is_required": True,
    },
    {
        "comment": "repository plugin id",
        "dtype": int,
        "name": "plugin_id",
        "name_xml": "@plugin_id",
    },
    {
        "comment": "human readable plugin name",
        "dtype": str,
        "i18n": True,
        "name": "name",
        "name_xml": "@name",
        "is_required": True,
    },
    {
        "comment": "short description of the plugin purpose only",
        "dtype": str,
        "i18n": True,
        "name": "description",
        "is_required": True,
    },
    {
        "comment": "longer description: how does it work, where does it install, how to run it?",
        "dtype": str,
        "i18n": True,
        "name": "about",
        "is_required": True,
    },
    {
        "comment": "comma separated, spaces allowed",
        "dtype": tuple,
        "importer": lambda x: tuple(x.split(",")),
        "exporter": lambda x: ",".join(x),
        "i18n": True,
        "name": "tags",
    },
    {
        "comment": "may be multiline",
        "dtype": str,
        "name": "changelog",
    },
    {
        "dtype": str,
        "name": "author",
        "name_xml": "author_name",
        "is_required": True,
    },
    {
        "dtype": str,
        "name": "email",
        "is_required": True,
    },  # author_email
    {
        "comment": "url to the plugin homepage",
        "dtype": str,
        "name": "homepage",
    },
    {
        "comment": "url to a tracker site",
        "dtype": str,
        "name": "tracker",
    },
    {
        "comment": "url to the source code repository",
        "dtype": str,
        "name": "repository",  # 'code_repository'
        "is_required": True,
    },
    {
        "comment": "path to the icon",
        "dtype": str,
        "name": "icon",
    },
    {
        "comment": "true if experimental, false if stable",
        "dtype": bool,
        "importer": str_to_bool,
        "exporter": lambda x: bool_to_str(x, style="truefalse"),
        "name": "experimental",
        "default_value": False,
    },
    {
        "comment": "true if deprecated, false if actual",
        "dtype": bool,
        "importer": str_to_bool,
        "exporter": lambda x: bool_to_str(x, style="truefalse"),
        "name": "deprecated",
        "default_value": False,
    },
    {
        "comment": "url for downloading the plugin",
        "dtype": str,
        "name": "download_url",
    },
    {
        "comment": "the zip file name to be unzipped after downloaded",
        "dtype": str,
        "name": "file_name",
    },
    {
        "comment": "dotted notation of minimum QGIS version",
        "dtype": QgsVersion,
        "importer": lambda x: QgsVersion.from_qgisversion(
            x, fix_plugin_compatibility=True
        ),  # TODO is it actually True?
        "exporter": lambda x: x.original,
        "name": "qgisMinimumVersion",
        "name_xml": "qgis_minimum_version",
        "is_required": True,
    },
    {
        "comment": "dotted notation of maximum QGIS version",
        "dtype": QgsVersion,
        "importer": lambda x: QgsVersion.from_qgisversion(
            x, fix_plugin_compatibility=True
        ),  # TODO is it actually True?
        "exporter": lambda x: x.original,
        "name": "qgisMaximumVersion",
        "name_xml": "qgis_maximum_version",
    },
    {
        "dtype": QgsVersion,
        "importer": QgsVersion.from_pluginversion,
        "exporter": lambda x: x.original,
        "name": "version",
        "is_required": True,
    },
    {
        "comment": "determines if the plugin provides processing algorithms",
        "dtype": bool,
        "importer": str_to_bool,
        "exporter": lambda x: bool_to_str(x, style="truefalse"),
        "name": "hasProcessingProvider",
        "default_value": False,  # TODO remove?
    },
    {
        "comment": "determines if the plugin provides functionallity for server",
        "dtype": bool,
        "importer": str_to_bool,
        "exporter": lambda x: bool_to_str(x, style="truefalse"),
        "name": "server",
    },
)

SPEC_DTYPES = tuple({field["dtype"] for field in SPEC})
NAME_XML = {
    field['name']: field['name_xml']
    for field in SPEC
    if field.get('name_xml', None) is not None
}
