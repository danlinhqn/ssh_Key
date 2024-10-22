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
    'danlinhqn': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDBO3RlQM1W5hmVrNKzPsy6/nJZvqsV0+Llsjkq+cqJNrJu7W9yGrS9hPq4YYueJLECc7gyJ1d5MGZNwD13tCd7slE6WDV1sboxeUJfUxy0jqbZe9C7GX3UD+Lm3V2bdlSMGq/1GV3yxWC0YxlUb0EPvzdylYXPae3vC79CRsa3mMsw5H36KjhkjOCP0nBELBIkVdOOH1+0u2hUZObOAXiGkEd8UvoI48JFWgsszWwfXCeSpX2BEM8Uh5Y18SWcNpmwzNsznEsrXeiTN4V6me9fI58AA1hmL39WBQjYvU7vUnurvs55VVworq+6cHyJxjsAwjnbO2/43Isav+Ze1igRH7AxHpHAG6QI11I3o5F2ZuhBv9bTPUIW6chHZrBpf7iDZKwfqOZ82FgQpMrELqMOedIydJ8qx/EAPB8XjYqBZSmJTJl5sY6eEcpsoLA8+hT5DLuBO9xcAGAE2esXhCU2JJ8IBEuCgEa4mCFP12YxaxYKfpf9RHLK1W4kRQoSSv5dIKkHeS04H4PsTEvAjkeOX7UjdPw+9ebjtZBEnGtltgWpLmbmzDE2s6uxN6pr5q3J8l3CPiMm9Jrgm5LK4cs/ji2hdMhA4k2o7wtZ38d01G22d3kAgeOpdTCSsLAKDqgUgHv9tXhac0NH60YpG9o43eTUDsAylbYzjy3bDqt4aQ== your_email@example.com',
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