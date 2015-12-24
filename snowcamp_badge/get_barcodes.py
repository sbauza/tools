#!/usr/bin/env python
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
import contextlib
import logging
import shutil
import sys

try:
    from urllib import request as urllib
except ImportError:
    # python2
    import urllib2 as urllib

URL = 'http://www.barcodes4.me/barcode/qr/qr.png?value=%s&size=5&ecclevel=3'


def fetch_image(uuid, dest='%s.png'):
    uuid = int(uuid)
    url = URL % uuid
    logging.debug(url)
    with contextlib.closing(urllib.urlopen(url)) as rd:
        rd_type = rd.headers['Content-Type']
        if rd_type != 'image/png':
            logging.warning("Go fock, this is not a PNG image")
            return
        with open(dest % uuid, 'wb') as wd:
                shutil.copyfileobj(rd, wd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="debug level",
                        action="store_true")
    parser.add_argument('uuid', nargs='+', help="UUID(s) to process")
    args = parser.parse_args()
    uuids = args.uuid
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    [fetch_image(uuid) for uuid in uuids]
