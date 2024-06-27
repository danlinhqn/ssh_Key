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
    'danlinhqn2': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDR2zgXI997Lp2ayA0KboPuTOS1Fk5vgwkvEbVwVHdgu4Nm4E3Yrsh09NGjY8nfVcNIYWEG+LzAh/2aljq0CAGPWYp2jC+3+WXQEP+iubpmWc8Hjvv0PQlL2d+8aBwvr6Cc8+xhg9X7FFrDdzM1F4CJSH0LUlyKz3UFlJftltgWlwpRGJB2QrnpudkE0fQWUvwR7c64PYtKgkXOsYwgkN709ECcqM4roay9AdTMzEGn9PbtF3kxL8LPRTMkC/sJ9C6tm9gbovF0+JUT9LS13ReEP9SMXxkZI5yyOVmj4lGhszVlQS6L8rSR2iqoI2XEXVt4UyVbWN2LcyDu5CVbfnblDLjyVaJFD18Ao4spJfPAnOuDRFO/7276LKF+zCs7ejU7S83lU7Fn/khgGpBhI4HZNvv2UP3VOYtsWJGop2Xvh8f2SIsVEergfRIeWEHQNNovkCBnB0LMoDu7Yf3BEMVs3azOrozIDdtQoXbxwzn0+OVHBaitclBFBoAEFsdF07UoDQLsn68AolqPlcphWwPcxWzEbPCGmBUQd0edX42tNGEBxAo/28Os5COQ0zxqhFdE/IzVFaFy6nPQfyklJNnHedniPErUjyInY+cSXT5cS4izYMrZ4IMkjlC+v3oYeartnT2rnqSP5QGCUq7o3MA0OOSz1l7lboIgHBQS8FEVkw== danlinhqn2@gmail.com',
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