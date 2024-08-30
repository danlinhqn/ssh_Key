#!/usr/bin/env python

'''
Script Create User for SnS
Author: TrungN

'''

import logging
import os, sys
import crypt
import random
import string

logging.basicConfig(level=logging.INFO)
PASSWORD_DEFAULT = "nUz76Xuf6yCXuYa"

class User():
    def __init__(self, user, password=PASSWORD_DEFAULT, pubkey=None, permission=None):
        self.user       = user
        self.password   = password
        self.pubkey     = pubkey
        self.permission = permission
        self.logger     = logging.getLogger('User')

    def __generate_pass(self, size = 15, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size)).lower()


    def create_user(self):
        encPass         = crypt.crypt(self.__generate_pass(),"22")
        try:
            status=os.system("useradd -p %s -s /bin/bash -d /home/%s -m %s" % (encPass, self.user, self.user))
            self.logger.info("Create user %s successful." % (self.user))
        except:
            self.logger.error("Create user %s failed with error %s." % (self.user, sys.exc_info()[1]))

    def add_pubkey(self):
        try:
            if self.pubkey:
                #Create .ssh directory
                home_path = "/home/%s/.ssh" % (self.user)
                if not os.path.exists(home_path):
                    os.mkdir(home_path)
                os.chmod(home_path, 0o700)
                #Add pubkey
                file_keys = "/home/%s/.ssh/authorized_keys" % (self.user)
                with open(file_keys, 'w') as f:
                    f.write(self.pubkey)
                os.chmod(file_keys, 0o600)
                os.system('chown -R %s.%s %s' % (self.user, self.user, home_path ))
            else:
                self.logger.error("User dont have pubkey to add")
        except:
            self.logger.error("Have some invalid with %s." % (sys.exc_info()[1]))

    def grant_sudoer(self, noPassword=False):
        if self.permission != 'root':
            return False
        try:
            if noPassword:
                os.system('echo "%s ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers' % (self.user))
            else:
                os.system('echo "%s ALL=(ALL) ALL" >> /etc/sudoers' % (self.user))
            self.logger.info('Grant sudoer permission for %s successful' % (self.user))
            return True
        except:
            self.logger.error('Grant sudoers permission for %s failed with'.format(self.user, sys.exc_info()[1]))

        return False

info_user = {
    'danlinhqn2': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC8pxMn5FpK1Y/O3u5KFtVjlFRYrwwjUWZ726AuYXz+Mx2fhcCPShU/9w0PY2s2XAEjYN+9UAnjEFKQL4jDSSqJwnwfow6bvCIj5Y805XuTza1vga5ChhyiKh6Lfvgfu/iVKy3oZQzSdIKhXhNC5VazZEWJ+dq4lyAk7ZAB/r/0LJymzWeAXCcY0o2kHne046hR3jppi2aDr2qNVLVbDk7gktd6ZQymw4aX2WD9te/rKy382rx5YQXMJB+F8aghjlSNdpkoahr/U81ysbPOFnGPr2cn7IOThgtsQ4fqKFXGo5hghBLLXH8NeFDu8OjRcGgzxH3C9A0KkeadMLBcWeJPz8NhjGAVl6O9C9+e0fC7V0z1kBoaxMfHHuxcF/Th0dCFdgzsQwYzJcnAHFwWXatu6c3V5ut4X3BNKqvxEGFe5tfC+EHyH3/YpWkpJSNicmuK4S/cpIHrQitVjAXApSSDiB+KmnwCvASUmjGm482pSt7RKGIJSgYsvQ+dSaxth3WT/wwWEXzkYTohEa/BzKFyxvli+k6vP9D6N80K1IMNSYc4gUbji59eCXi0wxexfpWsuO/UgyL0OCpJyRq7dU4cQzRNVzYWCu6zVq0CcGpySwnm0BSZ40Mio3zvTY27daaaJsnMruQPvSB+X8NvzLxbcL0XTzA6jzh2ZMAH7oWEBQ== opinvn@gmail.com',
}

logger = logging.getLogger(__name__)
if os.getegid() != 0:
    sys.exit("Only root can run this script.")

for k, v in info_user.items():
    logger.info('Create user %s with password default' % (k))
    user = User(k,pubkey=v, permission='root')
    user.create_user()
    user.add_pubkey()
    user.grant_sudoer(noPassword=True)
    print("---------------------------------------")