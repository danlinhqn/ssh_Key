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
    'danlinhqn': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDMnl2rjHbdfYMt1XyA3nIxoKCgZ+SU9HOXEAKH7JaGP0TVzqXnmIol43vTslFgx0kFGyYWTQjjO/K7LAzNr7B4GFXZ5GpIkybJgNTEuSfAgtgy7cdRGrcNFMevTZzATVHpBVzPqzPw71t079C3UQvesZdtMsf44b4Rvyrd+C1PipRJX9lbJ54NfmRjLVk4sR8TxjqgwZrjzyQeh9P8GDJkG29bYI6oKsk3AHIABou+p0fW3jxZXpnAA1Vqzuu8265FCxvGvAje9wz7xl1c6dNS37Xx9W5bY72RIzxtouWuXPCHTSdxteG4I9nbWunUI0ezLtv6DevYV2AYDK4T0GkHn/yiClEkoQZThzzrnWwdKDAmga1j5/aVADn26hAQBDuq70B/w2uXaeWAs8zmpR3JVWOWnzKqJ39/txSJ5lKI53G57avfcckAZHVvFk3+E2tSsh6jSfpZxf6x8RuPM5VbDwWqkyoB2Yr+8cN68pppyEbjLF+8wBr8Vg7jDBrBqn8ik+UP7VSs/Wa8EAZkXMatcgBC7JV9p/fKOswTQfJYIvE/mC9W0mB8l5Y5O1r1DzepWkZBzC8aSoYjmm6KEDEV5Y5j8wNOXG6jGsTbGcg8N0r0gKA/cWIuD1ZTd4n/d8pFTp5gbfrHO4Hx1S1CkkVdi1xiqA6ZmDR/1dVuWxdtvw== lucaslaptop@be.com',
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