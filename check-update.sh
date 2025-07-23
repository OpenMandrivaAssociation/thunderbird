#!/bin/sh
curl -s https://ftp.mozilla.org/pub/thunderbird/releases/ |grep /pub/thunderbird/releases |sed -e 's,.*/">,,;s,/.*,,' |grep '^[0-9.]*$' |sort -V |tail -n1
