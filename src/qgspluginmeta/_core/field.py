# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    src/qgspluginmeta/_core/field.py: Plugin meta data field type

    Copyright (C) 2017-2020 QGIST project <info@qgist.org>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU General Public License
Version 2 ("GPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
https://github.com/qgist/pluginmanager/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import typing

from .abc import QgsMetadataFieldABC
from .spec import SPEC_DTYPES

from typeguard import typechecked

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@typechecked
class QgsMetadataField(QgsMetadataFieldABC):
    """
    Represents one field of meta data

    Mutable.
    """

    def __init__(
        self,
        name: str,
        dtype: typing.Any,
        value: typing.Any = None,
        default_value: typing.Any = None,
        importer: typing.Union[None, typing.Callable] = None,
        exporter: typing.Union[None, typing.Callable] = None,
        is_required: bool = False,
        i18n: bool = False,
        known: bool = True,
        comment: str = "",
    ):

        if len(name) == 0:
            raise ValueError('"name" must not be empty.')
        if dtype not in SPEC_DTYPES:
            raise TypeError('"dtype" unknown or broken.')

        self._name = name
        self._dtype = dtype
        self._importer = importer
        self._exporter = exporter
        self._is_required = is_required
        self._value = None
        self._known = known  # is meta field a known one?

        self._i18n = i18n  # TODO unused
        self._comment = comment  # TODO unused

        if not self._is_valid_value(value) and value is not None:
            raise TypeError('"value" does not have matching tyspe.')
        if not self._is_valid_value(default_value) and default_value is not None:
            raise TypeError('"default_value" does not have matching tyspe.')

        self._value = value
        self._default_value = default_value

    def __repr__(self) -> str:

        return (
            "<QgsMetadata "
            f'name="{self._name:s}" '
            f'dtype={getattr(self._dtype, "__name__", str(self._dtype)):s} '
            f'set={"yes" if self.value_set else "no"} '
            f'known={"yes" if self._known else "no"} '
            f'i18n={"yes" if self._i18n else "no"} '
            f'required={"yes" if self._is_required else "no"}'
            ">"
        )

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # HELPER
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def _is_valid_value(self, value: typing.Any) -> bool:

        return isinstance(value, self._dtype)

    def _value_to_string(self, value: typing.Any) -> str:

        if self._exporter is None:
            return str(value)

        value_str = self._exporter(value)
        if not isinstance(value_str, str):
            raise TypeError('"value_str" must be a str.')
        return value_str

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # API
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def copy(self) -> QgsMetadataFieldABC:

        return type(self)(
            name=self._name,
            dtype=self._dtype,
            value=self._value,
            default_value=self._default_value,
            importer=self._importer,
            exporter=self._exporter,
            is_required=self._is_required,
            i18n=self._i18n,
            known=self._known,
            comment=self._comment,
        )

    def update(self, other: QgsMetadataFieldABC):

        if not isinstance(other, type(self)):
            raise TypeError('"other" is not a meta data field')
        if self.name != other.name:
            raise TypeError("name mismatch")
        if self.dtype != other.dtype:
            raise TypeError("dtype mismatch")
        if not other.value_set:
            return

        self.value = other.value

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # PROPERTIES
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def name(self) -> str:
        return self._name

    @property
    def dtype(self) -> typing.Any:
        return self._dtype

    @property
    def value_set(self) -> bool:
        return self._value is not None

    @property
    def default_value_set(self) -> bool:
        return self._default_value is not None

    @property
    def value(self) -> typing.Any:
        return self._value

    @value.setter
    def value(self, new_value: typing.Any):
        if not self._is_valid_value(new_value):
            raise TypeError('"new_value" does not have valid type')
        self._value = new_value

    @property
    def default_value(self) -> typing.Any:
        return self._default_value

    @property
    def value_string(self) -> str:
        if not self.value_set:
            raise ValueError("Nothing to export to string - value not set.")
        return self._value_to_string(self._value)

    @value_string.setter
    def value_string(self, new_value_str: str):
        if not isinstance(new_value_str, str):
            raise TypeError('"new_value_str" must be a str.')
        if self._importer is not None:
            new_value = self._importer(new_value_str)
        else:
            new_value = self._dtype(new_value_str)
        self.value = new_value

    @property
    def default_value_string(self) -> str:
        if not self.default_value_set:
            raise ValueError("Nothing to export to string - default_value not set.")
        return self._value_to_string(self._default_value)

    @property
    def is_required(self) -> bool:
        return self._is_required

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # PRE-CONSTRUCTOR
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @classmethod
    def from_unknown(cls, name: str, value: typing.Any) -> QgsMetadataFieldABC:

        return cls(name=name, value=value, dtype=type(value), known=False,)
