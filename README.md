# Dummy attester as a Gramine enclave

## Build the enclave (no SGX needed)

```
docker compose build
docker compose run --rm dummyattester
```

This builds the MRENCLAVE.
The Dockerfile build includes installing python venv packages, according to the requirements.txt. Python files from venv are copied from this venv, and then included in the enclave manifest. 

## Run the enclave in SGX

```
docker compose -f docker-compose-sgx.yml build
docker compose -f docker-compose-sgx.yml run --rm dummyattester run.sh
```

## Complete the EPID attestation (untrusted)
```
gramine-sgx-ias-request report -k $RA_API_KEY -q quote -r datareport -s datareportsig
```

## Verify the report (untrusted, this could be done in RAVE)
```
gramine-sgx-ias-verify-report -E $MRENCLAVE -v -r datareport -s datareportsig --allow-outdated-tcb
```