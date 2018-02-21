import blinker

signals = blinker.Namespace()

started = signals.signal('round-started')


def each(round, **kwargs):
    print 'Round {}'.format(kwargs.get('user').name)
    print 'Round {}'.format(round)


def round_two(round, **kwargs):
    print 'This is round 2: {}'.format(kwargs.get('user').name)
    print 'This is round 2: {}'.format(round)

    with open('C:\\Users\\Ricky\\Desktop\\Blinker.txt', 'w') as outfile:
        outfile.write('Hallo!')
        outfile.write('\r\n{}'.format(kwargs.get('user').name))


class User(object):
    def __init__(self):
        self.name = 'ricky'


if __name__ == "__main__":
    started.connect(each)
    started.connect(round_two, sender=2)
    ricky = User()
    print started.receivers
    started.send(2, user=ricky)

'''
###############################################################
# THIS WORKED TO CATCH SIGNALS
###############################################################

from flask_security.signals import password_changed
from datetime import datetime
def eacher(sender, **kwargs):
    print 'sender bitch!', sender
    with open('C:\\Users\\Ricky\\Desktop\\Blinker.txt', 'w') as outfile:
        print sender
        outfile.write('Reset Password')
        outfile.write('\r\n{}'.format(datetime.now()))
        outfile.write('\r\n{}'.format(kwargs.get('user').username))

password_changed.connect(eacher, weak=False)
print 'receivers bitch', password_changed.receivers



I was able to print out the connections and receivers here
def change_user_password(user, password):
    from flask_security.changeable import hash_password
    from flask_security.signals import password_changed
    """Change the specified user's password

    :param user: The user to change_password
    :param password: The unhashed new password
    """
    user.password = hash_password(password)
    g.datastore.modify_user(user)
    send_password_changed_notice(user)
    current_app.logger.debug('Connected to: {}'.format(password_changed.connected_to))
    current_app.logger.debug('Receivers: {}'.format(password_changed.receivers))
    password_changed.send(current_app._get_current_object(),
                          user=user)
'''
