from O365 import Account

SCOPES = ['message_send', 'message_all']


def send_email(account: Account, to: str, subject: str, body: str):
    """
    Function to send an email using Office 365 account.

    This function uses the user's Office 365 account to create a new message.
    It then sets the recipient, subject and body of the email message before sending the email.

    Parameters:

        account (O365.Account): The sender's Office 365 account.
        to (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The content of the email.

    The function does not return a value.
    """

    m = account.new_message()
    m.to.add(to)
    m.subject = subject
    m.body = body
    m.send()
