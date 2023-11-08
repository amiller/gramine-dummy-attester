import subprocess

cmd = "gramine-sgx ./python"
proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)

print("Writing to stdout")
proc.stdin.write(b"9113b0be77ed5d0d68680ec77206b8d587ed40679b71321ccdd5405e4d54a68200000000000000000000000000000000000000000000000000000000deadbeef\n")
proc.stdin.flush()
print("Reading from stdin")
quote = proc.stdout.readline()
print("Got quote")
print(quote)
