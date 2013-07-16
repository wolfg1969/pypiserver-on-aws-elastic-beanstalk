import errno
import os
import os.path as path
import random
import sys

try:
    import crypt
except ImportError:
    try:
        import fcrypt as crypt
    except ImportError:
        sys.stderr.write("Cannot find a crypt module.  "
                         "Possibly http://carey.geek.nz/code/python-fcrypt/\n")
        sys.exit(1)

import pypiserver

def salt():
    """Returns a string of 2 randome letters"""
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789/.'
    return random.choice(letters) + random.choice(letters)

CWD = os.getcwd()
PACKAGES = path.join(CWD, 'data')
HTPASSWD = path.join(CWD, 'htpasswd')

USER_PASS = os.environ['PARAM1']

if USER_PASS:

    f = open(HTPASSWD, 'w')

    lines = []
    for raw_user_passwd_pair in USER_PASS.split(','):
        user, raw_passwd = raw_user_passwd_pair.split(':', 2)
        password = crypt.crypt(raw_passwd, salt())
        lines.append("%s:%s\n" % (user, password))

    f.writelines(lines)
    f.close()

try:
    os.makedirs(PACKAGES)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

application = pypiserver.app(root=PACKAGES, password_file=HTPASSWD)
