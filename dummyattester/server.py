import socket
import sys
import subprocess

def server(host='0.0.0.0', port=8000):

    cmd = "gramine-sgx ./python"
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # TODO: temp port? use docker environment?
        s.bind((host,port))
        s.listen()
        while True:
            try:
                print(f"Server is listening on {host}:{port}")
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(128)
                        if not data: break

                        # Check hex conversion
                        print('Received data:', data)
                        data = data.decode('utf-8')
                        assert len(bytes.fromhex(data)) == 64

                        # Write
                        print('writing proc input')
                        proc.stdin.write(data.encode()+b'\n')
                        proc.stdin.flush()
                        
                        # Receive the quote
                        print('Reading procs output')
                        proc.stdout.flush()
                        quote = proc.stdout.readline()

                        # Quote is in hex, still write it in hex
                        print(quote)
                        conn.sendall(quote)
                        
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

if __name__ == '__main__':
    server()

