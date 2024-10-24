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
    'opinvn': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCYO2m+xV0WH6jY+pf62dT8CqC9Dy9/9Op7C8zUjV6aOKWxcpalyCRhaY2svM8lzS3tTa+vVVnNiV9wS+pIeXwagYxGbYdEfVRmGv7juDlFZhtzYgeDNuDAzx4C2lrk07PnpstY2erkB6VqzHeQC82iwHNtNRD2z4BZE3DEE3Sqyuz66dmw1qTxULWPpMPdNAIgtz8f7JyhzP4JKpwAZ/fsTaNnudDF4Bz+1Ssesc8YDo7HP5Cntn9PBD1rAD6DS+zN2mQXVT9ALnk0Euua/eT+kRXAzNYCuzAq46Jfa6kns+YbakJfO7GieNZ6jGk8kR1UMlEXZ2+awf3ZjRP0SA1eHGaUG9QXeng92X4k988Mnfh9spSe3H+pp/FzUcgorH4BvI4hHoELA75gykhcp1gK1wZ9mIIk+MzfDpKvdFimiHxajWqvtMlsnYMXs60YxsJ6iuZHIG47QeDSr231ZzJ9VIgcF8wGa88ajjjhwxzSspW/ijVSPvQywkm3gRqds+o2nlrMb+ZJpz8CHrLT4yoovljeRdsmaJmO1S6fLpsrXts163I1HZSwbuWFD5B2GHqb8Lzx65ppPm9GFpq0UplFW/VQZ3+QJOr3+Ny6VMN1DKIJkGmJkU+dNf4XiE+ApY3kXzJDLYBp/+Ky43d3clMLsoiEukQZf9VvTmlQ7gfpyw== danlinhqn@example.com',
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