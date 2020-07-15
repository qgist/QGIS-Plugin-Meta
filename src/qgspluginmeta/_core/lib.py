# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    src/qgspluginmeta/_core/lib.py: Library

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

from typeguard import typechecked

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def str_to_bool(value: str) -> bool:

    if value.lower() in ('yes', 'true', '1'):
        return True
    if value.lower() in ('no', 'false', '0'):
        return False

    if any((value.lower().startswith(item) for item in ('yes', 'true'))):
        return True
    if any((value.lower().startswith(item) for item in ('no', 'false'))):
        return False

    raise ValueError(f'value "{value:s}" can not be converted to bool')

@typechecked
def bool_to_str(value: bool, style: str) -> str:

    styles = {
        'TrueFalse': lambda x: 'True' if x else 'False',
        'truefalse': lambda x: 'true' if x else 'false',
        'YesNo': lambda x: 'Yes' if x else 'No',
        'yesno': lambda x: 'yes' if x else 'no',
        '10': lambda x: '1' if x else '0',
        }

    if style not in styles.keys():
        raise ValueError(f'style "{style:s}" is unknown')

    return styles[style](value)
