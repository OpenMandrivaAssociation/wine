#!/bin/sh
# Wine is a bit of a special case because we can update it only when
# the corresponding wine-staging patchset is released as well...
curl -s -L https://raw.githubusercontent.com/wine-staging/wine-staging/master/staging/VERSION |head -n1 |sed -e 's,.* ,,g'

