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
    'anhtran': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC19/EIM58iAn8S+0M532M6ELltByQgQcJO++Sfx6NKFYyF9cWSzQwR7wVNsdkHugB/OslJuta2PcDFwCQdbjJkFA5ZF0ZeOlQE71j8hEDsE7sklAiTF/WnDAZOfQ1yABg790SIWIaIFM8yiAnwtfrACmFXHTZoNMCJ/i5KkoUoPvHKgVnF7OPEron3UMqgYt1rZHs7J1t2KBcLmYsgBj/N7AhajifDmZLqJTjPXVHtW/L2UnvOd0Tux0TdhDf+NV2fI7bEG/PMpi1S+nIbFpVIun0CUhwnrIQtQx7t3kLRZsv0p2shfX/v/8KHw7Y8Ynr3hskOX+7eTDdsSpY5w9RCkkLYyrL8x8lqSIhzPz8OQV6XZWMtoaESKUlvNVYvN182MIYpvHksqEq7ITsblYHFtiONIEheqse6nseChVVbritSA5SsYvYcglyWrTCeKsUE76GaOpPCGQnz51V3mX/ejqBa3nYUovnKGepN37FNajgph58aj1YHkg9Y1AkuL92rk5HwBoxwpKgC0Po2W5yxbjt9yNUvqQiAbnpI0wIbr1HKQ5bimTjI/YMC8leShZAjxWWSnHFVitWimeSfwThOUtYQuAb1tiBQYbuNQOVVlipGTwrHuaqoxzWl2ZTodD1HYuUgsg9Vs3/u6Bp29reMB19QIoqWb8HGj24DMNK2uQ== thien@AnhTran',
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