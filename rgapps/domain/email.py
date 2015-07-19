"""rgapps.domain.email module

This module contains Email functionality.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["EMail"]

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib

from validate_email import validate_email

from rgapps.config import ini_config


class EMail:
    """A EMail class to send emails
    """

    def send_email(self, recipient, subject, message):
        """Sends given message using Gmail credentials defined in the
        configuration file.

        Parameters
        ----------
        recipient:  str (required)
            recipient email address
        subject:  str (optional)
            email subject
        message: str (optional)
            message to send

        Returns
        -------
            nothing.

        Raises
        ------
        ValueError:
            The recipient email emails in the settings is invalid
        SMTPHeloError:
            The server didn't reply properly to the helo greeting.
        SMTPAuthenticationError:
            The server didn't accept the username/password combination.
        SMTPException:
            No suitable authentication method was found.
        SMTPRecipientsRefused:
          The server rejected ALL recipients (no mail was sent).
        SMTPSenderRefused:
            The server didn't accept the from_addr.
        SMTPDataError:
            The server replied with an unexpected error code (other than a
            refusal of a recipient).
        """

        # ensure valid GMail Account
        is_valid = validate_email(ini_config.get("Email", "GMAIL_ACCOUNT"))

        if(not is_valid):
            raise ValueError("GMail Account [{0}] is not valid email address"
                             .format(ini_config.get("Email", "GMAIL_ACCOUNT")))

        gmail_user = ini_config.get("Email", "GMAIL_ACCOUNT")
        gmail_password = ini_config.get("Email", "GMAIL_PASSWORD")

        logging.debug("Sending email using Gmail account [{0}]  "
                      "to recipient [{1}]"
                      .format(gmail_user, recipient))

        is_valid = validate_email(recipient)

        if(not is_valid):
            raise ValueError("Recipient [{0}] is not valid email address"
                             .format(recipient))

        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        logging.debug("Sending email to [{0}] usgin Gmail account [{1}]"
                      .format(recipient, gmail_user))

        mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail_server.login(gmail_user, gmail_password)
        failed_recipients = mail_server.sendmail(
            gmail_user, recipient, msg.as_string()
        )

        if failed_recipients:
            logging.warn("Email failed to following recipients [{0}]"
                         .format(failed_recipients))

        mail_server.close()

        return


if __name__ == '__main__':
    pass