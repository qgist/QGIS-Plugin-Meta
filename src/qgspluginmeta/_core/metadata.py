# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    src/qgspluginmeta/_core/metadata.py: Plugin meta data type

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

from configparser import ConfigParser
import io
import typing

from typeguard import typechecked

from .abc import QgsMetadataABC, QgsMetadataFieldABC
from .spec import SPEC, NAME_XML
from .field import QgsMetadataField

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: META DATA
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@typechecked
class QgsMetadata(QgsMetadataABC):
    """
    Meta data of one single plugin

    Mutable.
    """

    def __init__(self, **import_fields: typing.Union[None, str]):
        """
        `import_fields` is a dict of keys (field names, type `str`) and values (field values, all type `str`).
        """

        self._fields = {field["name"]: QgsMetadataField(**field) for field in SPEC}

        for key in import_fields.keys():
            if import_fields[key] is None:
                continue
            if key not in self._fields.keys():
                self._fields[key] = QgsMetadataField.from_unknown(
                    key, import_fields[key]
                )
            else:
                self._fields[key].value_string = import_fields[
                    key
                ]  # Import of values of known fields and type cast happens here!

        self._id = self._fields["id"].value

    def __repr__(self) -> str:

        return f'<QgsMetadata id="{self._id:s}">'

    def __getitem__(self, name: str) -> QgsMetadataFieldABC:

        if not isinstance(name, str):
            raise TypeError('"name" must be a str')
        if name not in self._fields.keys():
            raise KeyError('"name" is not a valid meta data field')

        return self._fields[name]

    def keys(self) -> typing.Generator[str, None, None]:

        return (key for key in self._fields.keys())

    def required_fields_present(
        self,
        ignored_fields: typing.Union[
            typing.Tuple[str],
            typing.List[str],
            typing.Generator[str, None, None],
            typing.Iterator[str],
        ] = None,
    ) -> bool:
        "`email` is required but e.g. not exposed in plugins.xml from plugins.qgis.org - can be ignored"

        if ignored_fields is None:
            ignored_fields = tuple()

        ignored_fields = tuple(ignored_fields)

        for field_id in self._fields.keys():
            if all(
                (
                    not self._fields[field_id].value_set,
                    self._fields[field_id].is_required,
                    field_id not in ignored_fields,
                )
            ):
                return False

        return True

    def update(self, other: QgsMetadataABC):
        "Similar to dict.update, update this metadata with content from other metadata"

        if self["id"].value != other["id"].value:
            raise ValueError("id mismatch")

        for key in other.keys():
            if key == "id":
                continue
            if key not in self.keys():
                self._fields[key] = other[key].copy()
            else:
                self._fields[key].update(other[key])

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # EXPORT
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def as_dict(self) -> typing.Dict[str, str]:
        "Export meta data to JSON-serializable dict (strings)"

        return {
            field_id: field.value_string
            for field_id, field in self._fields.items()
            if field.value_set
        }

    def as_xmldict(self) -> typing.Dict[str, str]:
        "Export meta data to dict for XML export"

        xml_dict = self.as_dict()  # TODO bools / exporters ...

        xml_dict["file_name"] = f'{xml_dict["id"]:s}.{xml_dict["version"]:s}.zip'
        xml_dict.pop("id")
        xml_dict["@version"] = xml_dict["version"]

        for name, name_xml in NAME_XML.items():
            xml_dict[name_xml] = xml_dict.pop(name)

        return xml_dict

    def as_metadatatxt(self) -> str:
        "Export meta data as metadata.txt string"

        txt_dict = self.as_dict()  # TODO bools / exporters ...
        txt_dict.pop('id')

        cp = ConfigParser(
            interpolation=None,  # TODO ok? Because of e.g. tuflow.3.0.4.zip (containing `%` in changelog)
            strict=False,  # TODO ok? Because of e.g. Sentinel-2 Download 3.5 (field `email` twice)
        )
        cp["general"] = txt_dict

        with io.StringIO() as f:
            cp.write(f)
            f.seek(0)
            metadatatxt_string = f.read()

        return metadatatxt_string

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # PRE-CONSTRUCTOR
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @classmethod
    def from_xmldict(
        cls, xml_dict: typing.Dict[str, typing.Union[str, None]],
    ) -> QgsMetadataABC:
        "Fixes an XML dict from xmltodict and returns a meta data object"

        xml_dict = xml_dict.copy()

        if xml_dict["@version"] != xml_dict["version"]:
            raise ValueError("One single plugin release has two versions")
        xml_dict.pop("@version")

        for name, name_xml in NAME_XML.items():
            xml_dict[name] = xml_dict.pop(name_xml)

        if "id" not in xml_dict.keys():
            if "file_name" not in xml_dict.keys():
                raise KeyError(
                    'Neither "id" nor "file_name" in XML meta data - no way to determine plugin id'
                )
            if not xml_dict["file_name"].lower().endswith(".zip"):
                raise ValueError(
                    'Unusual value for "file_name", does not end on ".zip"'
                )
            if xml_dict["version"] not in xml_dict["file_name"]:
                raise ValueError('Version is not part of "file_name"')
            xml_dict["id"] = xml_dict["file_name"][
                : -1 * (len(".zip") + len(xml_dict["version"]) + len("."))
            ]

        return cls(**xml_dict)

    @classmethod
    def from_metadatatxt(
        cls, plugin_id: str, metadatatxt_string: str
    ) -> QgsMetadataABC:
        "Parses a metadata.txt string and returns a meta data object"

        cp = ConfigParser(
            interpolation=None,  # TODO ok? Because of e.g. tuflow.3.0.4.zip (containing `%` in changelog)
            strict=False,  # TODO ok? Because of e.g. Sentinel-2 Download 3.5 (field `email` twice)
        )

        try:
            cp.read_string(metadatatxt_string)
        except Exception as e:
            raise ValueError(f"failed to parse metadata.txt: {str(e):s}")

        try:
            general = cp["general"]
        except Exception as e:
            raise ValueError(
                f'failed to fetch section "general" from metadata.txt: {str(e):s}'
            )

        try:
            fields = dict(general)
        except Exception as e:
            raise ValueError(
                f'failed to convert section "general" from metadata.txt to dict: {str(e):s}'
            )

        return cls(id=plugin_id, **fields)
