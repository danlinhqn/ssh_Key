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
    'minh.ha': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC4EXieVth7vKhVzd0Kw+rxcdCl6mT3qx8VHk35e1SrOAdyw9JbEMosKKPGyJw6lm7o6l/tJDPqnWtcoQWReavmRPbyI1LmBis3y9uqsw6B2xJdoFx99/CnXmiLY7Ajqs6i3FqWPgqJIFNDvjcof3cYYtE2S1vTI7C89KrWLSiJOCnF3l9Aah9BK7Pbn4p1ALuWtsHarHoT90XPWx6K9RF9dEwn/7bmrR++v9Lct+j9vzwBmP0iz7OqRNW26KpQiVYEmqm2OAcqHN4u4yMp4rZoS3fRw/SKxtJo0M7a8SDEXzHvqFJMzAYVdjfh5c7ShuyIPTNofevRgPV2Io0eD8D6pCize50Ef7Rpo1WnN1V1JCe3pEc8uiE83dEB27FjmAI2kvih1ZRa7wPHh0RVlwLQ0O/OnFwOcRBqFsgJ/cC3gq//47qBFK7opkjB4+3S8oGrn/tdlzS0OH6aE2qKB8BmXFjCkqoYpw+sYVqp2I1kQsz9yAvuRSc1/KMdXryZcDmQ0ZyewGftDvu4D+4SGtTwJlPb3/lVPRzLAPkatA78FtWXtQyGzf/7Bbf0hrzaywuAoK0BbDi2MQTyGAQxwZY2xfFP6Vj+7KcsrGNhOyFjDZj91f9+fIKwODduWH/HTlFzpf1hThaVYryDuWWJjkWimJhVg6sY4Utg+vfAzkz6Bw== your_email@example.com',
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