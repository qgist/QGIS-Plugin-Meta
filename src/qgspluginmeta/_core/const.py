# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    src/qgspluginmeta/_core/const.py: Constants

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
# VERSIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

VERSION_PREFIXES = (
    "VERSION",
    "VER.",
    "VER",
    "V.",
    "V",
    "REVISION",
    "REV.",
    "REV",
    "R.",
    "R",
)
VERSION_UNSTABLE_SUFFIXES = (
    "ALPHA",
    "BETA",
    "PREVIEW",
    "RC",
    "TRUNK",
)
VERSION_DELIMITERS = (
    ".",
    "-",
    "_",
    " ",  # TODO commas, i.e. `,`?
)
