from flask import Flask, Response
import os
import socket
from subprocess import check_output
import tempfile
import json

app = Flask(__name__)

RA_CLIENT_SPID = os.environ['RA_CLIENT_SPID']
RA_API_KEY = os.environ['RA_API_KEY']
CMD_HOST=os.environ['CMD_HOST']
CMD_PORT=8000

CMD_HOST2=os.environ['CMD_HOST2']

@app.route("/dcap/<userreportdata>")
def serverdcap(userreportdata):
    assert len(userreportdata) == 128
    assert len(bytes.fromhex(userreportdata))==64
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((CMD_HOST2,CMD_PORT))
    s.sendall(userreportdata.encode())

    f = s.makefile()
    quote = f.readline().strip()

    fpname = './testquote'
    with open('./testquote','wb') as fp:
        fp.write(bytes.fromhex(quote))
        fp.flush()
        cmd = f'gramine-sgx-quote-view ./testquote'
        out = check_output(cmd, shell=True)
        print(out)
    
    return Response(out + quote.encode(), mimetype='application/json')

@app.route("/<userreportdata>")
def server(userreportdata):
    assert len(userreportdata) == 128
    assert len(bytes.fromhex(userreportdata))==64

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((CMD_HOST,CMD_PORT))
    s.sendall(userreportdata.encode())

    f = s.makefile()
    quote = f.readline().strip()

    fpname = './testquote'
    with open('./testquote','wb') as fp:
    #with tempfile.NamedTemporaryFile() as fp:
        # fpname = fp.name
        fp.write(bytes.fromhex(quote))
        fp.flush()
        # Two more named files?
        cmd = f'gramine-sgx-ias-request report -g {RA_CLIENT_SPID} -k {RA_API_KEY} -q {fpname} -r ./datareport -s ./datareportsig'
        out = check_output(cmd, shell=True)
        print(out)

    datareport = open('./datareport').read()
    datareportsig = open('./datareportsig').read().strip()
    obj = dict(report=json.loads(datareport), reportsig=datareportsig)
    
    return Response(json.dumps(obj).replace(' ',''), mimetype='application/json')
