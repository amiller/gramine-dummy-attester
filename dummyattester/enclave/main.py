import sys
import json
import hashlib

while True:
    line = sys.stdin.readline()

    obj = line.split()
    assert len(obj) == 2
    # Address String
    address = obj[0]
    message = obj[1]
    sha2hash = hashlib.sha256(obj[0] + obj[1])

    with open("/dev/attestation/user_report_data", "wb") as f:
        f.write(sha2hash)

    with open("/dev/attestation/quote", "rb") as f:
        quote = f.read()
    
    # Sha2 hash
    sys.stdout.write(quote.hex() + '\n')
