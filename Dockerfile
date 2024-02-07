ARG GRAMINE_IMG_TAG=dcap-595ba4d
FROM ghcr.io/initc3/gramine:${GRAMINE_IMG_TAG}

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
ENV VENV_PATH=/root/.venvs/gramine

RUN apt-get update && apt-get install -y python3-venv npm software-properties-common jq netcat
RUN python3.9 -m venv $VENV_PATH

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /

# Option A: Installing python dependencies from requirements.txt
# Compilation to .pyc is not reproducible. So we don't do this in the enclave.
COPY requirements.txt requirements.txt 
RUN $VENV_PATH/bin/pip install --no-compile -r requirements.txt

ARG RA_TYPE=epid
ENV RA_TYPE=$RA_TYPE
ARG RA_CLIENT_SPID=51CAF5A48B450D624AEFE3286D314894
ENV RA_CLIENT_SPID=$RA_CLIENT_SPID
ENV RA_API_KEY=669244b3e6364b5888289a11d2a1726d
ENV RA_API_KEY=$RA_API_KEY
ARG RA_CLIENT_LINKABLE=1
ENV RA_CLIENT_LINKABLE=$RA_CLIENT_LINKABLE

ARG DEBUG=0
ENV DEBUG=$DEBUG
ARG SGX=1
ENV SGX=$SGX

ADD ./dummyattester/ /gramine-dummy-attester/dummyattester
ADD ./scripts /gramine-dummy-attester/dummyattester/scripts

WORKDIR /gramine-dummy-attester/dummyattester
RUN mkdir -p input_data output_data enclave_data

RUN make SGX=$SGX RA_CLIENT_LINKABLE=$RA_CLIENT_LINKABLE DEBUG=$DEBUG RA_TYPE=$RA_TYPE RA_CLIENT_SPID=$RA_CLIENT_SPID

CMD [ "gramine-sgx-sigstruct-view", "python.sig" ]
