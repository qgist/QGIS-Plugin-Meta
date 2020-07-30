# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    tests/lib.py: Test support library

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

import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_txts():

    data_fld = os.path.join(os.path.dirname(__file__), 'data')
    fns = [fn for fn in os.listdir(data_fld) if fn.startswith('metadata_') and fn.endswith('.txt')]

    for fn in fns:
        with open(os.path.join(data_fld, fn), 'r') as f:
            txt = f.read()
        plugin_id = fn.split('_', 1)[1].rsplit('_', 1)[0]
        plugin_version = fn.rsplit('_', 1)[1].rsplit('.', 1)[0]
        yield plugin_id, plugin_version, txt
