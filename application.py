import errno
import os
import os.path as path

import pypiserver
from passlib.apache import HtpasswdFile

CWD = os.getcwd()
PACKAGES = path.join(CWD, 'data')
HTPASSWD = path.join(CWD, 'htpasswd')

USER_PASS = os.environ['PARAM1']
if USER_PASS:
    ht = HtpasswdFile(HTPASSWD)
    for raw_user_password_pair in USER_PASS.split(','):
        user, password = raw_user_password_pair.split(':', 2)
        ht.set_password(user, password)

    ht.save()


try:
    os.makedirs(PACKAGES)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

application = pypiserver.app(root=PACKAGES, password_file=HTPASSWD)
