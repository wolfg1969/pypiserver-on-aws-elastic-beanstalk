import errno
import os
import os.path as path

import pypiserver

CWD = os.getcwd()
PACKAGES = path.join(CWD, 'data')
HTPASSWD = path.join(CWD, 'htpasswd')

USER_PASS = os.environ['PARAM1']

if USER_PASS:

    f = open(HTPASSWD, 'w')

    f.writelines([line for line in USER_PASS.split(',')])
    f.close()

try:
    os.makedirs(PACKAGES)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

application = pypiserver.app(root=PACKAGES, password_file=HTPASSWD)
