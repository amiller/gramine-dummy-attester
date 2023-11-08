# Dummy attester as a Gramine enclave

## Build the enclave (no SGX needed)

```
docker compose build
docker compose run --rm dummyattester
```

This builds and prints the MRENCLAVE.

## Use a web service to fetch a dummy attestation and check it

While best effort lasts, this is a server that returns dummy attestations on arbitrary report data.
```
docker compose exec dummyattester bash
curl http://dummyattest.ln.soc1024.com/9113b0be77ed5d0d68680ec77206b8d587ed40679b71321ccdd5405e4d54a6820000000000000000000000000000000000000000000000000000000000000000 | bash scripts/fetchandverify.sh 
```

## Verify the report (untrusted, this could be done in RAVE)
```
gramine-sgx-ias-verify-report -E $MRENCLAVE -v -r datareport -s datareportsig --allow-outdated-tcb
```

## Run the enclave in SGX

This command will run the enclave once and output a json object containing a quote
```
docker compose build
docker compose -f docker-compose-sgx.yml run --rm dummyattester bash run.sh
```

## Complete the EPID attestation (untrusted)
```
gramine-sgx-ias-request report -k $RA_API_KEY -q quote -r datareport -s datareportsig
```
