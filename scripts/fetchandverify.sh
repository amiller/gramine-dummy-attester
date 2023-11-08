#!/bin/bash

cat <&0 > report.json
cat report.json | jq -c .report | tr -d '\n' > datareport
cat report.json | jq -r .reportsig > datareportsig
gramine-sgx-ias-verify-report -E 0000000000000000000000000000000000000000000000000000000000000000 -v -r datareport -s datareportsig --allow-outdated-tcb
