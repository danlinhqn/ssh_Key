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
    'duc.nguyen': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDTtF42YS4oHA0LOsYSWGxqubRKhQfjDicfS5+yCPtVFr3O7tqcJi+44BSQO6RTH4eG97M0E5xG5XFYeEZZKBVlXLki1l+9FxK+Hlo9Q4tyfo9WnohJ3xOTig5W8jltfQeqOuEgU6vsRXpmq9rngn42byCcRjekyk6UffsrDwJX5+S2kMVTl/HTq9YIucYVkU9EYLrtM2aWffZti6781Ejim7Vp/bvwyAgI+IslJK7fYc6sl51oO7tSockEIFKzDUPlPjJnkVnm38KdPfrNY+KqA6Xilef0YyIEUoM4NJ17j1JIP3ldiowtXMqOMqQ8SU/DBkoBOrxzuyGSK7h8g90lAG41KCcD2NmgGktZl9IfYxw4i8Dvgm5DfEVAA62n24t7d+qzxKtq18p1ECXC2hxm7d9bOj86PdAV6E9PKcMH0F+QSLOkFXtQ7FYRcs6rBF0vlYibZbEQHiXppmBKVDoBn0df5JSgOtsk386w33fCbGoav3JEdt5i2QIwczBaCas= danie@DucNguyen',
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