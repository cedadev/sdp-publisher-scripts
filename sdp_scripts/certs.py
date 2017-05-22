import os
import re
import sys
import time
from myproxy.client import MyProxyClient
import OpenSSL.crypto as crypto

import utils

def load_certificate(certificate_file):
    f = open(certificate_file)
    data = f.read()
    f.close()
    return crypto.load_certificate(crypto.FILETYPE_PEM, data)


def have_in_date_certificate(certificate_file, time_margin=3600):
    """
    Returns boolean, whether certificate exists and does not expire until 
    current time plus a margin.
    """
    try:
        x509 = load_certificate(certificate_file)
    except (IOError, crypto.Error):
        return False

    earliest_permitted_expiry = time.strftime("%Y%m%d%H%M%SZ", time.gmtime(time.time() + time_margin))

    return x509.get_notAfter() > earliest_permitted_expiry


def get_certificate(hostname, username, password, lifetime=None):
    """
    returns a myproxy certificate string
    hostname can contain optional ":port"   
    """
    client_args = {}
    if lifetime:
        client_args['proxyCertLifetime'] = lifetime * 3600
    try:
        pos = hostname.index(":")
        client_args['hostname'] = hostname[:pos]
        client_args['port'] = int(hostname[pos + 1 :])
    except ValueError:
        client_args['hostname'] = hostname

    myproxy = MyProxyClient(**client_args)
    return myproxy.logon(username, password)
    

def read_creds_file(creds_file):
    """
    Read simple creds file which just consists of hostname, username, password on separate lines.
    Leading / trailing whitespace gets removed.
    """
    if os.stat(creds_file).st_mode & 077:
        raise Exception("refusing to use {0} - remove all group and world permissions".format(creds_file))
    f = open(creds_file, "r")
    creds = []
    for i in range(3):
        line = f.readline()
        m = re.match("\s*(.*)\s*$", line)
        creds.append(m.group(1))
    f.close()
    return tuple(creds)
    

def ensure_certificate(certificate_file, creds_file, lifetime=None, log=sys.stdout.write):
    """
    Test if in date certificate file exists. If it doesn't, go get one.
    """

    if have_in_date_certificate(certificate_file):
        log("using existing certificate {0}".format(certificate_file))
        return

    log("refreshing certificate {0}:".format(certificate_file))

    log("  reading credentials")
    hostname, username, password = read_creds_file(creds_file)

    log("  getting certificate using host={0}, username={1}".format(hostname, username))
    creds = get_certificate(hostname, username, password, lifetime)

    log("  creating certificate file")
    utils.ensure_parent_dirs(certificate_file)
    fout = open(certificate_file, "w")
    os.fchmod(fout.fileno(), 0600)
    for cred in creds:  
        fout.write(cred)
    fout.close()


if __name__ == '__main__':
    import config
    ensure_certificate(config.certificate_file,
                       config.credentials_file,
                       config.certificate_lifetime)

