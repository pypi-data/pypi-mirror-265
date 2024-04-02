from temp_mails import Tempmail_org as Mail

mail = Mail()
assert mail.email != "", "Mail name empty"
print(mail.email)
d0 = mail.get_inbox()
print(d0)
assert len(d0) <= 1, "Inbox not empty"

d1 = mail.wait_for_new_email()
print(d1)
d2 = mail.wait_for_new_email()
print(d2)

assert d1["_id"] != d2["_id"], "Email IDs are the same"

assert len(mail.get_inbox()) == 2, "Inbox length wrong"

d3 = mail.get_mail_content(mail_id=d1["_id"])
print(d3)
assert d3 != None, "Failed to get email content"