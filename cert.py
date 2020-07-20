from flask import Flask, jsonify
import os
import sys
from os import environ


app = Flask(__name__)

app.DATA_DIR = '/certs'
app.password = environ.get('ca_key_password')  

@app.route('/client/new', methods=['GET', 'POST'])
def generateSSLCert():
    if not os.path.exists(os.path.join(app.DATA_DIR, 'ca.key')) or not os.path.exists(os.path.join(app.DATA_DIR, 'ca.crt')):
        return("no ca cert found, trying to generating cert and key now")
    try:
        from OpenSSL import crypto, SSL

        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)

        cert = crypto.X509()
        cert.get_subject().C = "DE"
        cert.get_subject().ST = "Berlin"
        cert.get_subject().L = "Berlin"
        cert.get_subject().O = "My Company AG"
        cert.get_subject().OU = "My Department"
        cert.get_subject().CN = "Client Cert for MyService"
        cert.get_subject().emailAddress = "ssl@example.com"
        cert.set_serial_number(100)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)

        ca_crt = crypto.load_certificate(crypto.FILETYPE_PEM, open(os.path.join(app.DATA_DIR,'ca.crt')).read())
        cert.set_issuer(ca_crt.get_subject())

        cert.set_pubkey(k)
        ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(os.path.join(app.DATA_DIR,'ca.key')).read(), passphrase=app.password.encode('ascii'))
        cert.sign(ca_key, 'sha256')
        resp = (crypto.dump_certificate(crypto.FILETYPE_PEM, cert) + crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

        return resp,200, {'Content-Type': 'text/css; charset=utf-8'}

    except Exception as e:
        return(str(e))

if __name__ == '__main__':

  app.run(
    host = "0.0.0.0",
    port = 5000,
    debug = 0
  )
