# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    src/qgspluginmeta/_core/version.py: Version data type

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

import re
import typing

from typeguard import typechecked

from .abc import QgsVersionABC
from .const import (
    VERSION_PREFIXES,
    VERSION_UNSTABLE_SUFFIXES,
    VERSION_DELIMITERS,
)
from .error import QgsVersionValueError

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@typechecked
class QgsVersion(QgsVersionABC):
    """
    Allows to represent and compare versions (of QGIS and plugins)

    For compatibility, this follows most logic of QGIS' `python/pyplugin_installer/version_compare.py`.

    Immutable.
    """

    def __init__(self, *elements: str, original: typing.Union[None, str] = None):

        self._elements = elements
        self._original = original if original is not None else ".".join(elements)

    def __repr__(self) -> str:

        return f'<QgsVersion {str(self):s} ("{self._original:s}")>'

    def __str__(self) -> str:

        return ".".join(self._elements)

    def __getitem__(self, index: int) -> str:

        if index < 0 or index >= len(self):
            raise IndexError(
                f"following index out of bounds: {index:d} (0 ... {len(self)-1:d})"
            )

        return self._elements[index]

    def __len__(self) -> int:

        return len(self._elements)

    def __eq__(self, other: QgsVersionABC) -> bool:

        if len(self) != len(other):
            return False

        return all(((a == b) for a, b in zip(self._elements, other._elements)))

    def __ne__(self, other: QgsVersionABC) -> bool:

        return not self.__eq__(other)

    def __lt__(self, other: QgsVersionABC) -> bool:

        if self.__eq__(other):
            return False

        return self._greater_than(other, self)

    def __gt__(self, other: QgsVersionABC) -> bool:

        if self.__eq__(other):
            return False

        return self._greater_than(self, other)

    def __le__(self, other: QgsVersionABC) -> bool:

        if self.__eq__(other):
            return True

        return self.__lt__(other)

    def __ge__(self, other: QgsVersionABC) -> bool:

        if self.__eq__(other):
            return True

        return self.__gt__(other)

    @property
    def original(self) -> str:

        return self._original

    @property
    def stable(self) -> bool:

        for suffix in VERSION_UNSTABLE_SUFFIXES:
            if suffix in self._elements:
                return False

        return True

    @classmethod
    def _greater_than(cls, a: QgsVersionABC, b: QgsVersionABC) -> bool:
        "Compare two *unequal* versions a and b: Is a greater then b?"

        # set the shorter string as a base length
        base_len = len(a) if len(a) < len(b) else len(b)

        # try to determine within the common/base length
        for index in range(base_len):
            relation = cls._compare_elements(a[index], b[index])
            if relation != 0:
                return relation == 1

        # if the lists are identical till the end of the shorther string, try to compare the odd tail
        # with the simple space (because the 'alpha', 'beta', 'preview' and 'rc' are LESS then nothing)
        if len(a) > base_len:
            return cls._compare_elements(a[base_len], " ") == 1
        if len(b) > base_len:
            return cls._compare_elements(" ", b[base_len]) == 1

        # if everything else fails, compare original strings
        return a.original > b.original

    @classmethod
    def _compare_elements(cls, x: str, y: str) -> int:
        "Compare version element x with version element y (0/==, 1/>, 2/<)"

        if x == y:
            return 0

        is_numeric = (
            lambda element: len(element) > 0
            and element.isnumeric()
            and element[0] != "0"
        )
        rank_string = (
            lambda element: "Z" + element
            if element not in VERSION_UNSTABLE_SUFFIXES
            else element
        )

        # try to compare as numeric values (but only if the first character is not 0):
        if is_numeric(x) and is_numeric(y):
            return 1 if int(x) > int(y) else 2

        # if the strings aren't numeric or start from 0, compare them as a strings:
        # but first, set ALPHA < BETA < PREVIEW < RC < TRUNK < [NOTHING] < [ANYTHING_ELSE]
        return 1 if rank_string(x) > rank_string(y) else 2

    @staticmethod
    def _normalize_version_str(version_str: str) -> str:
        "Remove possible prefix from given string and convert to uppercase"

        if len(version_str) == 0:
            return ""

        version_str = version_str.upper().strip(" \t\n")
        for prefix in VERSION_PREFIXES:
            if version_str.startswith(prefix):
                version_str = version_str[len(prefix) :].strip(" \t\n")

        return version_str

    @staticmethod
    def _split_version_str(version_str: str) -> typing.List[str]:
        "Convert string to list of numbers and words"

        # return 0 for delimiter, 1 for digit and 2 for alphabetic character
        char_type = (
            lambda char: 0
            if char in VERSION_DELIMITERS
            else (1 if char.isdigit() else 2)
        )

        elements = [version_str[0]]
        for index in range(1, len(version_str)):
            if char_type(version_str[index]) == 0:
                pass
            elif char_type(version_str[index]) == char_type(version_str[index - 1]):
                elements[-1] += version_str[index]
            else:
                elements.append(version_str[index])

        for element in elements:
            if len(element) == 0:
                raise ValueError("splitting elements failed, element of zero-length")

        return elements

    @classmethod
    def from_pluginversion(cls, plugin_version_str: str) -> QgsVersionABC:
        "Parse plugin version string and return version object"

        if len(plugin_version_str) == 0:
            raise QgsVersionValueError("version must not be empty")

        plugin_version = cls._split_version_str(
            cls._normalize_version_str(plugin_version_str)
        )

        return cls(*plugin_version, original=plugin_version_str)

    @classmethod
    def from_qgisversion(
        cls, qgis_version_str: str, fix_plugin_compatibility: bool = False
    ) -> QgsVersionABC:
        "Parse QGIS version string and return version object"

        if len(qgis_version_str) == 0:
            raise QgsVersionValueError("version must not be empty")

        fragments = qgis_version_str.split('.')

        if len(fragments) > 3:
            raise QgsVersionValueError(
                "no valid QGIS version because too many fragments"
            )
        if any((not fragment.isnumeric() for fragment in fragments)):
            raise QgsVersionValueError(
                "no valid QGIS version because of non-numeric fragments"
            )

        while len(fragments) < 3:
            fragments.append('0')
        x, y, z = fragments

        # Return current QGIS version number as X.Y.Z for testing plugin compatibility.
        # If Y = 99, bump up to (X+1.0.0), so e.g. 2.99 becomes 3.0.0
        # This way QGIS X.99 is only compatible with plugins for the upcoming major release.
        if fix_plugin_compatibility and y == "99":
            x = str(int(x) + 1)
            y = z = "0"

        return cls(x, y, z, original=qgis_version_str)
