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
    'opinvn': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCy08zmPW0g5iBRGdr5WcV2PhTyjQ1yymqrd3MKHivVPn/TBafAt/KAcaJ2nfmoYpZQ+AAQFOD4u72SaqBGsQclMRZqlG6j+tQk72sN0mAQtl16fDm+9+t3MR6KLQHzvhdXexiGkxf5l3rsjxZP0kzsWnI1xVUaNNf9ofXKgcQAxSL7jtZYwvgYQzkW/qIJQzZynBdoGB79IcUO55wlCobdyguqfkh3FYF3/pTFBbxrYdtZEaAfV4Z4utstiHl/LzqI9Mre42PaMIVQ+LZagvosHLDyx0Oa6GoPUEggMrXsDxUoVvOy/0qbSefOITSzuZIzG2fSlIiH6UkrV/yFyEV5savtbHpxji8FRvi4enybZmMmtnQzpi92WBKY4Jk+QcGYsFx/QbobF2DEob4SfN2Tm5B9IB7OqkqVumQ06K/QY7+8ihsWdkDorWECkBWsP46oj3XJ4MTxK+Am9m9J58tiBA2mBD0qKGTpRk0ME5Fyne/wjR39x11nfi+Mly7rGPEmlWOQXTOzhtYcBqd0gfroY/IDC0AJdD+oJugv5NrANn4+g+q7UwZQ9d0ZKxPpBXXIEsm/cPPmQbLGZieF8skR+UX6qhl0woqN88pO5iXETSrFety3gf/8huzQcHzmrCoQk+5xuj+jplBcMJwXTqbAiNkS/FFdylGm69dcAtlFFw== actso@ActsoneVN',
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