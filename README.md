# Dummy attester as a Gramine enclave

## Build the enclave (no SGX needed)

```
docker compose build
docker compose run --rm attester
```

This builds the MRENCLAVE.
The Dockerfile build includes installing python venv packages, according to the requirements.txt. Python files from venv are copied from this venv, and then included in the enclave manifest. 

## Run the enclave in SGX

```
docker compose -f docker-compose-sgx.yml build
docker compose -f docker-compose-sgx.yml run --rm attester gramine-sgx ./python
```