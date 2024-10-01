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
    'danlinhqn': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC03lAS6YQ9nYlginnSvgR0D0TBqWB+/FKjA7tSgrYgED+H/+H/JVjnZFN99ljTxsYe0llA5vZFn2al+mw0R5e1tDEoMvTcTrTPjklU6TylMw18kvTxe/2DPteGAofma3DJB/Nsyxd8uVloLdMB22/5OVBz6JaXk/6hWvRxOd6dpe9KOe1XqMnx0H1UswqaTGx8NuJy94s5YCdzN+kcQ8+BgXbQ7WXhCJPCkpWR3U6b0lOBz1fH/Gc5DHUv5AmqmtUKtEbI1vowr7N0yKgKJx2lKH0hm0Q272gCOGWIe3Oy+54C5yXz/38qjz11tEbNfxPls92Uswe0mWKnlJ9CRe0KzKW9CB6Kb3p5G5cXgUtYJ/aabDiXuLTI/n91Hc1IgQWN7DpOXzlFC74sGZIYoZ1sBFPtRoUk6RNz5KtiOZLSySKGaK6WCh/OMjLzz65NKGB9UBgL/RF7MppKbZsLi/fv80LWqdU7qVT8bm8LGF7qtD496H6to2JFjrqLTcz5k04CJka4HTbQlobHpqj+Xua1B2qh5LYMRsSTP0XUH/ARn6fB+yFS0YL6eG2QFXhfaF3KQNSmJzOH6KiDsot6B8Islrp2AzR+irZM2QiVz39BZfAEdMnUq/tuWb8W4L8hkoL5HzJ17mlceKVM3UGrdIM1VXT+Tkj2YTpqA3kr3qTUcQ== your_email@example.com',
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