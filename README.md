# FyMail

FyMail is a shortcut for *F*ind *Y*our e*Mail*. It is a simple tool to search for email addresses in a given
account with a given provider.

## Quick Start

```py
fymail = FyMail()
email = await fymail.get(iden="zhongjiajie", provider="github", auth=token)
```

Two lines to get the email address of a user, see whole example in [tutorial.py](./examples/tutorial.py)

## Bulk Search

see whole example in [bulk.py](./examples/bulk.py)
