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

import io
import zipfile
import os
import sys
import xml

import requests
from tqdm import tqdm
import xmltodict


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TESTS_FLD = "tests"
TESTDATA_FLD = os.path.join(TESTS_FLD, "data")
REPO_DEFAULT_URL = "https://plugins.qgis.org/plugins/plugins.xml"

VERSIONS = {
    1: [8],
    2: [minor for minor in range(0, 19)] + [99],
    3: [minor for minor in range(0, 14+1)],
}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def make_testdata():

    for major, minors in VERSIONS.items():
        for minor in minors:
            print(f'-> QGIS {major:d}.{minor:d}')
            _fetch_data(major, minor)


def _fetch_data(major, minor):

    r = requests.get(f"{REPO_DEFAULT_URL:s}?qgis={major:d}.{minor:d}")
    data = r.text

    data_fixed = data.replace(
        "& ", "&amp; "
    )  # From plugin installer: Fix lonely ampersands in metadata

    try:
        tree = xmltodict.parse(data_fixed)
    except xml.parsers.expat.ExpatError:
        print('XML broken')
        return

    with open(os.path.join(TESTDATA_FLD, f"plugins_{major:d}-{minor:02d}.xml"), "w") as f:
        f.write(data)

    for node in tqdm(tree["plugins"]["pyqgis_plugin"]):

        assert node["version"] == node["@version"]
        assert node["file_name"].endswith(".zip")
        assert node["version"] in node["file_name"]

        node_id = node["file_name"][
            : -1 * (len(".zip") + len(node["version"]) + len("."))
        ]

        meta_fn = os.path.join(
            TESTDATA_FLD, f"metadata_{node_id:s}_{node['version']:s}.txt"
        )
        if os.path.exists(meta_fn):
            continue

        try:
            r = requests.get(node["download_url"])
        except:
            print(node)
            if r.status_code == 404:
                print("HTTP 404")
                continue
            raise

        data = r.content

        try:
            with io.BytesIO(data) as f:
                with zipfile.ZipFile(f, "r") as fz:
                    meta = fz.read(f"{node_id:s}/metadata.txt").decode("utf-8")
        except KeyError as e:
            print(node, 'missing metadata.txt')
            continue

        with open(meta_fn, "w") as f:
            f.write(meta)

        # print(f'{REPO_DEFAULT_URL:s}?package_name={node_id:s}&qgis=3.{minor:d}')
        # r = requests.get(f'{REPO_DEFAULT_URL:s}?package_name={node_id:s}&qgis=3.{minor:d}')
        # data = r.text
        #
        # with open(
        #     os.path.join(TESTDATA_FLD, f"plugins_3-{minor:02d}_{node_id:s}.xml"), "w"
        # ) as f:
        #     f.write(data)


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
