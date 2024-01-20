from O365 import Account

SCOPES = ['message_send', 'message_all']


def send_email(account: Account):
    m = account.new_message()
    m.to.add('ismaelbeli.com@gmail.com')
    m.subject = 'Testing!'
    m.body = "George Best quote: I've stopped drinking, but only while I'm asleep."
    m.send()