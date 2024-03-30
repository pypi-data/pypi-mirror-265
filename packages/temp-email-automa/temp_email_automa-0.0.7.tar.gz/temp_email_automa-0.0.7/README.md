A Python package for generating and interacting with temporary email addresses.

## Installation

You can install the package via pip:

```python
pip install temp_email_automa
```

## Usage

Import the `TempMail` class from the package:

```python
from temp_email_automa.main import TempMail
```

Create an instance of `TempMail` with optional parameters for login and domain. If not provided, a random email address will be generated:

```python
temp_mail = TempMail(login="example", domain="example.com")
```

You can also generate a random email address using:

```python
temp_mail.generate_random_email_address()
```

To get the email address generated or provided:

```python
email_address = temp_mail.email
```

You can get a list of active domains for email addresses using:

```python
active_domains = temp_mail.get_list_of_active_domains()
```

To retrieve a list of emails in the mailbox:

```python
emails = temp_mail.get_list_of_emails()
```

Retrieve a single email by its id:

```python
email_id = 1  # Example id
single_email = temp_mail.get_single_email(email_id)
print(single_email)
```

## Data Structures

The package provides a `Email` data class representing an email message with the following attributes:

- `id`: str
- `sender`: str
- `subject`: str
- `date`: str
- `body`: str
- `textBody`: str
- `htmlBody`: str

Example:

```python
from dataclasses import dataclass

@dataclass
class Email:
    id: str
    sender: str
    subject: str
    date: str
    body: str
    textBody: str
    htmlBody: str
```
