from temp_mails import Etempmail_com as Mail
from random import choice


domain = choice(Mail.get_valid_domains()) #bc some domains are down atm

mail = Mail(domain=domain)
print(mail.email)
assert mail.email != "", "Mail name empty"
assert mail.email.endswith(domain), "Mail does not match the used mail"

d0 = mail.get_inbox()
print(d0)
assert len(d0) == 0, "Inbox not empty"

d1 = mail.wait_for_new_email()
print(d1)
d2 = mail.wait_for_new_email()
print(d2)

assert len(mail.get_inbox()) == 2, "Inbox length wrong"
