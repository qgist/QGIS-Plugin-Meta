# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    makefile.py: Handling build and test stuff

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
import sys

import requests


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TESTS_FLD = "tests"
TESTDATA_FLD = os.path.join(TESTS_FLD, "data")
REPO_DEFAULT_URL = "https://plugins.qgis.org/plugins/plugins.xml"

MINOR_MIN = 8
MINOR_MAX = 14
MINOR_STEP = 2


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def make_testdata():

    for minor in range(MINOR_MIN, MINOR_MAX + MINOR_STEP, MINOR_STEP):
        r = requests.get(f"{REPO_DEFAULT_URL:s}?qgis=3.{minor:d}")
        with open(
            os.path.join(TESTDATA_FLD, f"plugins_all_3-{minor:02d}.xml"), "w"
        ) as f:
            f.write(r.text)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ENTRY POINT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def main():

    assert len(sys.argv) > 1

    if sys.argv[1] == "testdata":
        make_testdata()
    else:
        raise NotImplementedError()


if __name__ == "__main__":

    main()
