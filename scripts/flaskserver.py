from flask import Flask, Response
import os
import socket
from subprocess import check_output
import tempfile
import json
import base64
import eth_abi
from binascii import hexlify

app = Flask(__name__)

RA_CLIENT_SPID = os.environ['RA_CLIENT_SPID']
RA_API_KEY = os.environ['RA_API_KEY']
CMD_HOST=os.environ['CMD_HOST']
CMD_PORT=8000

CMD_HOST2=os.environ['CMD_HOST2']


@app.route("/forge-epid/<userreportdata>")
def serverforge(userreportdata):
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

    datareport = open('./datareport').read()
    datareportsig = open('./datareportsig').read().strip()
    obj = dict(report=json.loads(datareport), reportsig=datareportsig)
    report = obj['report']
    items = (report['id'].encode(),
             report['timestamp'].encode(),
             str(report['version']).encode(),
             report['epidPseudonym'].encode(),
             report['advisoryURL'].encode(),
             json.dumps(report['advisoryIDs']).replace(' ','').encode(),
             report['isvEnclaveQuoteStatus'].encode(),
             report['platformInfoBlob'].encode(),
             base64.b64decode(report['isvEnclaveQuoteBody']))
    abidata = eth_abi.encode(["bytes", "bytes", "bytes", "bytes", "bytes", "bytes", "bytes", "bytes", "bytes"], items)
    sig = base64.b64decode(obj['reportsig'])
    return Response(hexlify(eth_abi.encode(["bytes","bytes"], (abidata,sig))), mimetype='application/json')


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

    datareport = open('./datareport').read()
    datareportsig = open('./datareportsig').read().strip()
    obj = dict(report=json.loads(datareport), reportsig=datareportsig)
    
    return Response(json.dumps(obj).replace(' ',''), mimetype='application/json')
