# temp-mails

#### A basic wrapper around various temp mail sites, aiming to provide an almost identical api for every site.

The main purpose of this is to provide an easy way to use different temp mail services with almost the same api, meaning little refactoring is needed.\
If there are any issues, please send me an email (bertigert@riseup.net) or create an issue, i cant test every email for every change I or the host makes.
## Installation
While every python3 version _should_ hypothetically work, python 3.12 is best
```
pip install temp-mails
```
### Requirements
```
pip install requests beautifulsoup4 lxml websocket-client
```
Note that you may need to uninstall all websocket packages in order for websocket-client to function properly

## Supported Sites (46)
- https://10minemail.com/ - semi-official
- https://10minutemail.com/ - unofficial
- https://internxt.com/temporary-email - unofficial
- https://www.minuteinbox.com/ - unofficial
- https://temp-mail.io/ - unofficial
- https://temp-mail.org/ - semi-official
- https://temp-mailbox.com/ - unofficial
- https://10minutesemail.net/ - unofficial
- https://etempmail.net/ - unofficial
- https://www.disposablemail.com/ - unofficial
- https://www.emailondeck.com/ - unofficial
- https://1secmail.com/ - official
- https://www.mohmal.com/en/inbox - unofficial
- https://www.fakemail.net/ - unofficial
- https://tempmail.email/ - unofficial
- https://tempmail.plus/ - unofficial
- https://generator.email/ - unofficial
- https://cryptogmail.com/ - unofficial
- https://mail.tm/ - official/semi-official
- https://temp-inbox.com/ - unofficial
- https://mailhole.de/ - unofficial
- https://tmailor.com/ - unofficial
- https://tmail.ai/ - unofficial
- https://cloudtempmail.com/ - unofficial
- https://luxusmail.org/ - unofficial
- https://muellmail.com/ - unofficial
- https://tempmail.gg/ - unofficial (server down?)
- https://www.eztempmail.com/ - unofficial, captcha
- https://tempail.com/ - unofficial, captcha
- https://tempmail.ninja/ - unofficial
- https://upxmail.com/ - unofficial (server down?)
- https://www.trash-mail.com/ - unofficial
- https://tempemailfree.com/ - unofficial
- https://tempr.email/ - unofficial
- https://tempmail.net/ - unofficial
- https://www.guerrillamail.com/ - semi-official
- https://tm-mail.com/ - unofficial
- https://tempmail.lol/ - official
- https://yopmail.com/ - unofficial, captcha
- https://etempmail.com/ - unofficial
- https://tmail.gg/ - unofficial
- https://mailtemp.uk/ - unofficial
- https://mostakbile.com/ - unofficial
- https://fakermail.com/ - unofficial, untested
- https://tempmails.net/ - unofficial
- https://temp-mail.gg/ - unofficial

### In Progress
- ...

> unofficial = we use no official API, because the website does not offer one (at least for free)\
> semi-official = website hat an official API, but we don't use it, often because it is using RapidAPI or broken\
> official = we use the websites official API (RapidAPI or not)
> captcha = requires you to go onto the website and solve a captcha/verify your browser on the same IP. After that it should work for some requests/minutes.

## Usage

Create an email on the site https://10minemail.com/
```python
from temp_mails import Tenminemail_com

mail = Tenminemail_com() # Generate a random email address
print(mail.email) # get the name of the email (e.g. example@examplehost.com)

print(mail.get_inbox()) # get all emails in the inbox

data = mail.wait_for_new_email(delay=1.0, timeout=120) # wait for a new email for 120 seconds and get the email data
print(data)

print(mail.get_mail_content(message_id=data["_id"])) # get the content of the email
```

The wrapper api for each email host is very similar, so little refactoring is needed in order to change the email host. However, the email data may change in format or similar. One email host could just return a string with the html content of the email, another one could return a dict with subject, content etc, I will probably add better support for that at some point.\
Also note that only some hosts support user defined names/domains.\
Also note that the built in wait_for_mail can break if there are too many emails or too many emails at once. You can implement you own custom function for that case. It works for all my use cases though (registrations).

### Websites I won't add at the moment
- https://www.emailnator.com/ - would be RapidAPI, site doesnt rly work
- https://smailpro.com/ - would be RapidAPI, site doesnt rly work
- https://maildrop.cc/ - uses cloudflare
- https://www.throwawaymail.com/en - server down
- https://www.tempmail.us.com/ - 1 email/IP, uses cpanel