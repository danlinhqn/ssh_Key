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
    'openvpn_home': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCfD4D7OeAQSZF2Ig6BrG/u/zBPiN3V5foSVCWowpDvRSTJn2P7pnUKQZ8BHiWoDxhTJKHErQUzUWDDbyQV7LZGBiNH3I/oXMD7aQGdu9N2CnfhPVpKqpt+YZa8dlBrjFeAwu3xIImWWxn2yEIpx9y5W99j6GFn31KJ1SizFjMhyJUG5loCrvlB0W+LPdjfZY4xg1z19xws/XWp9ViOyXD+0aLpaxeAKyBUP5a8xQHKgDyxV3l0MknJd6AQtDBrvclk8WbFFLYi6OFQYMlHdoNeqCFEB22QNa7c+b9BTbf1dczRMuBrqkwZlr6ufJpKW+IZtLhOhp9U0SILABewdv5x1dl5h/4masm4M3SCMj5rql2N/SJhY/TfJ/VOgRoB6VzKhTwjOa/D23yrzu+IV5lTVkFSIrYloTrhllaCOQbwdlk1/yc0lft1spxbHbte/rbUgclEGwYxfHUUlQ2Nl0aapzBpjz7PUePeV4yt/fMEzKQV9J0Y+tVlMqIe31QTcQUSxKOW3QOA4WYZ5Z8B0fvBbt6+4HWWjxaKLaDsVwl52CNDnPl4S1uPgPuS2gIflAmNQRfE7KQKY4ZQXhnjcopoJJndNSX1Xj9e1+fK8h3RZ+aAtzEYcOcJ296+nBDl4LfwGsgV2Sk+vppSnV8fjyPZCV62ULfvTe7ccrnObh95fw== opinvn@gmail.com',
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