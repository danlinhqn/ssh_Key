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
    'khai': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDhOKS2OoPhrzpaAKw4Qn6z58FWF7TbCWNelimLKVLpJ1SFy35xp9mJC/WPLmyZAryREWwAPIPF3g1GctIJtIvg5PxauFS9/i8jaoN564KP6GgxZ4deZ5NZAtoDV9IP6DIz7TcLS+MlaQ6pHGEA6KutPDTMYVRpQZMi82WbvQE6qBwOvpo83oUIySYp78J+rZ2Ska+dOJf4LEfGsjV7jPeOzCADlYQBkrf1SFxT+Q5193KR34qDxAXo8ANUaV5YETSCsurO4pgaLVMOfz+SR3yUATz/X237FrlxPJgvTBoQ8hB6Yglem7bk7kBNmv5sg+liHX+UX8ecJx/GfpOzybrKXC9vKdagUFaToaJlYyBZcU5516vven3JQyo3S9TXJaz5vN78cq8OeFwYNZJJGpgHzf0GtgxXNOuj2TiWGECDp8tlNx0PaZB+uA3hSjSRqCDs1Fq+YB9NpjQxomttHfBSC8xs2CySyjR3JvNuQMBgBoBVqyTMOj1RzzGL1t0FsLZmyiUw+ytJmnYIvXlK6+G6pul5U1uuqf+Ol5Nzr9dDxxwyGTCeQW0Oq12AZd/vmz1hUjP6A6GULCqg0y01toXyq6NqPmZJat5k6am7ct/gRStPUqP1YZe7ohuYSarttK2jM8kI8fP7/+CLCuXDb48WVJY/tKSDOjBtdHfGhQoqIw== anhpowerpc@MSI',
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