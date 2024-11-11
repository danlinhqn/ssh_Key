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
    'opinvn': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCUZdjbfjL0Dv7jbGNMcd04aZYGWkTTDi9XphKntmF6JbnrCwxXibpEhNt2t3m8Ifg0JUiAJGsLRMAGM4AD4EXGt6CPhEzWWS5XreHIWlTT2FW5mqxCFlBsJ6gWkbxwTI9z44VmBWQ1yu/nHvXpJ6qcxPylehsl+P9Lxc5qCKKDHPdwCfa8a0DsQDBCClTz3A9hyBkp0nYG+gtdtyKJrYjD6vlaVyvMisXAuKj/LB6b692tMIT8kY6uxTSGELmkOIfbQ+Jj4ou+Om5G7CkkSiz3NKiEurKvj+QBhvtD0uf0s0C1eAe1P7piQwsEHxEU/P155aeIs8gp1LVsT0pM2CwgA1Gcp++v569+YgYuVrE3sJlAtGLkYSWM0C6C0AOXB7pSIsRL5qOYZmWo1Fzft7/1Gysdrzd/rCrkJKZo0sfuWJX5JNKGO8+5610bdWL39/PLErJBnxhBbeSvKFx6YqafIczKvxQk2fZCRWeR+6sscL8mZ3tHGtPqdhTC3tq9mif0//P6d1ofZjsBrJy3zijpEx2gTUQxr5VjH6UeFr/I/IY7s/WHQiqU9leQEzwmFiLMwGRduYu2FGjovLunQLFO+FBXHIPAtaBz87IDyT142vrGc6ViO6rIPFVGml7S+JLcPpjHkNfAD6W2/n9edAFtYW/xcldbMSLwd6lE8UNkYQ== your_email@example.com',
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

#