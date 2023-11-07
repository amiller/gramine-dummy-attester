#!/usr/bin/env bash

set -e
set -x

if [[ "$SGX" == 1 ]]; then
    GRAMINE="gramine-sgx ./python"
elif [[ "$SGX" == -1 ]]; then
    GRAMINE="python"
else
    GRAMINE="gramine-direct ./python"
fi

INPUT_PATH=/gramine-dummy-attester/dummyattester/input_data
OUTPUT_PATH=/gramine-dummy-attester/dummyattester/output_data

mkdir -p "${INPUT_PATH}/leak/"

cd /gramine-dummy-attester/dummyattester

$GRAMINE -m enclave.make_graph

# === SGX quote ===
if [[ "$SGX" == 1 ]]; then
    $GRAMINE -m enclave.sgx-report &> OUTPUT
    grep -q "Generated SGX report" OUTPUT && echo "[ Success SGX report ]"
    $GRAMINE -m enclave.sgx-quote &>> OUTPUT
    grep -q "Extracted SGX quote" OUTPUT && echo "[ Success SGX quote ]"
    cat OUTPUT
    gramine-sgx-ias-request report --api-key $RA_TLS_EPID_API_KEY --quote-path "${OUTPUT_PATH}/quote" --report-path ias.report --sig-path ias.sig
fi

echo "done"
 
