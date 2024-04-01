import smtplib
import traceback
import sys


class Mailer:

    def __init__(self, smtp_server, username, password, from_mail_address, smtp_port=465,):

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.from_mail_address = from_mail_address

        self._username = username
        self._password = password

        self.server = smtplib.SMTP_SSL(host=smtp_server, port=smtp_port)
        self.server.set_debuglevel(True)
        self.server.esmtp_features['auth'] = 'LOGIN PLAIN'

    def send_mail(self, to_mail_address, message_header, message_body):

        message = f'From: {self.from_mail_address}\r\n' \
                  f'To: {to_mail_address}\r\n' \
                  f'Subject: {message_header}\r\n' \
                  f'\r\n' \
                  f'{message_body}\r\n'

        try:

            server = smtplib.SMTP_SSL(host=self.smtp_server, port=self.smtp_port)
            server.set_debuglevel(True)
            server.esmtp_features['auth'] = 'LOGIN PLAIN'
            server.login(self._username, self._password)
            server.sendmail(self.from_mail_address, to_mail_address, str(message))
            server.quit()

        except smtplib.SMTPServerDisconnected:
            print("smtplib.SMTPServerDisconnected")
        except smtplib.SMTPSenderRefused:
            print("smtplib.SMTPSenderRefused")
        except smtplib.SMTPRecipientsRefused:
            print("smtplib.SMTPRecipientsRefused")
        except smtplib.SMTPDataError:
            print("smtplib.SMTPDataError")
        except smtplib.SMTPConnectError:
            print("smtplib.SMTPConnectError")
        except smtplib.SMTPHeloError:
            print("smtplib.SMTPHeloError")
        except smtplib.SMTPAuthenticationError:
            print("smtplib.SMTPAuthenticationError")
        except smtplib.SMTPResponseException as e:
            print("smtplib.SMTPResponseException: " + str(e.smtp_code) + " " + str(e.smtp_error))
        except Exception as e:
            print(f"Exception: {e}")
            traceback.format_exc()
            print(sys.exc_info()[0])
