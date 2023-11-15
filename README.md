# Dummy attester as a Gramine enclave

The enclave itself only interacts on stdin/stdout.
It runs in a loop, expecting to receive a 128 byte message on stdin, and producing a quote in response.
It therefore has an extremely simple interface.

To make it more practical, this also comes with a socket server `dummyattester/server.py`. This runs on the same docker container, but outside the enclave. In fact it invokes the gramine process, thus having access to its stdin/stout. Outside the docker environment I also include a flask server.

## Build the enclave (no SGX needed)

```
docker compose build
docker compose run --rm dummyattester
```

This builds and prints the MRENCLAVE.
Currently this is `e3c2f2a5b840d89e069acaffcadb6510ef866a73d3a9ee57100ed5f8646ee4bb`


## Use a web service to fetch a dummy attestation and check it

While best effort lasts, this is a server that returns dummy attestations on arbitrary report data.
```
docker compose run --rm dummyattester bash -c \
 "curl http://dummyattest.ln.soc1024.com/9113b0be77ed5d0d68680ec77206b8d587ed40679b71321ccdd5405e4d54a6820000000000000000000000000000000000000000000000000000000000000000 | bash scripts/fetchandverify.sh"
```

To see how this server works look at `flaskserver.py` (run outside the docker environment) and `dummyattester/server.py` (run inside the docker environment).

## Verify the report (untrusted, this could be done in RAVE)
From within the docker container (or if you have e:
```
gramine-sgx-ias-verify-report -E 000000000000000000000000000000000000 -v -r datareport -s datareportsig --allow-outdated-tcb
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


## Running a server
```
docker compose -f docker-compose-sgx.yml run --detach dummyattester python server.py
# TODO: how to find the ip addr of docker compose?
docker inspect gramine-dummy-attester-dummyattester-run-c95f0bc336da | grep IPAddress
CMD_HOST=172.18.0.2 flask --app flaskserver run --host 0.0.0.0
```