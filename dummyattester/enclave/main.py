import sys
import hashlib

if __name__ == '__main__':
    while True:
        # Read a message specifying a user report data (64 bytes)
        line = sys.stdin.readline()
        hexreportdata = line.strip()
        assert len(hexreportdata) == 128
        
        # TODO: abi encoding?
        # Address String
        message = bytes.fromhex(hexreportdata)

        # Set the user data
        with open("/dev/attestation/user_report_data", "wb") as f:
            f.write(message)

        # Read the quote
        with open("/dev/attestation/quote", "rb") as f:
            quote = f.read()

        # Write the quote
        sys.stdout.write(quote.hex() + '\n')
        sys.stdout.flush()
        
