#!/bin/sh
curl https://www.thunderbird.net/en-US/ 2>&1 |grep download.mozilla.org |grep os=linux64 |head -n1 |sed -e 's,.*product=thunderbird-,,;s,-.*,,'
