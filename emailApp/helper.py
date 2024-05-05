

from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def send_email(emailData):
    subject    =  emailData['subject']
    message    = emailData['message']
    from_email = emailData['from_email']
    recipient_list = emailData['recipient_list']
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.send()

def send_html_email(emailData):
    subject        = emailData['subject']
    from_email     = emailData['from_email']
    recipient_list = emailData['recipient_list']

    # Load HTML content from a template
    html_content = get_template('email_template.html').render({'context_variable': 'value'})

    email = EmailMultiAlternatives(subject, 'Text content', from_email, recipient_list)
    email.attach_alternative(html_content, 'text/html')

    '''
    # Attach a file
    email.attach_file('path/to/your/file.txt')
    '''
    email.send()

  