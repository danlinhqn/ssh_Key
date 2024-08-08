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
    'kali_home': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCsFmZOPu+LQPvhAGNTTa3Ytb+gb2YHBCRhkZ65p8aNrcMhIELkVGHvbqci9x4QG+N9wp93vdKjTGtgzaOu4xAm50XGeqTK4EWJs0N91oKKxHiHQznRwxEwhqZr2EuiHHntUdoTlR2lPBNUpwBSgglZO5dacVzaxxRDefvNaLJsP0XIzC8kcHqLy78EyZBsHls9u/sywmocwXGBMu2Tr3KOjEtBorjZAoRFNgEwLasBGud7+7/YXrOLoF5M0VvJeOi0oox4Ayuv/AVYMoBolHpMbYCRaiHoNtuXf8Hls4kmt4uZWdXn1C0nbVKfl55Onx68Y/4o5CETxkdWSBywqCU+y9WO5XroFNWwiEzCKuWqkFRnmaTy/v5tgw1uxJeq57DUZIxZF2ORDTn9gCNgytFc+uFUeefj5+9Wt9BwHSV7cMu/LSIxOtwu0cg/5R8ZtVmTgnC3aikVnwsnPvBwxMkUupHZZ6Fz06LYyt1wi4AKCkvOFBZVHkGyeQ2sAfCdG5ufBK8mWZHSqnMoSpJBQMj/BMvtfVW8hcplil5knjw/bAVn34eFXLRoV/VjDkHkgWWFLjnplp/sI0XhbUolalNUUsZ/OoyuiEwnEVeR+tXi/ZBHbWY0A6MjNLqjYyNuSYt7476AuM9gVrKYPPE7OqJ1rJip9+h57iOZKYCI1s+ikw== opinvn@gmail.com',
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