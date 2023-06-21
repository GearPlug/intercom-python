# intercom-python
![](https://img.shields.io/badge/version-0.1.1-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*intercom-python* is an API wrapper for intercom, written in Python.  
This library uses Oauth2 for authentication.
## Installing
```
pip install intercom-python-2
```
## Usage
```python
# if you have an access token:
from intercom.client import Client
client = Client(access_token=access_token)
```
```python
# if you are using Oauth2 to get an access_token:
from intercom.client import Client
client = Client(client_id=client_id, client_secret=client_secret)
```
To obtain and set an access token:
1. **Get authorization URL**
```python
url = client.authorization_url(redirect_uri)
```
2. **Get access token using code**
```python
response = client.get_access_token(code)
```
3. **Set access token**
```python
client.set_token(access_token)
```
Check more information about Intercom Oauth: https://developers.intercom.com/building-apps/docs/setting-up-oauth
#### Get current user
```python
me = client.get_current_user()
```
#### List all admins
```python
admins = client.list_all_admins()
```
#### List data attributes
```python
# model options are: contact, company, conversation
data_atts = client.list_data_attributes(model, include_archived=False)
```
#### List tags
```python
tags = client.list_tags()
```
### Contacts
#### - List all contacts
```python
contacts = client.list_all_contacts()
```
#### - Filter contacts
```python
# field options: https://developers.intercom.com/intercom-api-reference/reference/searchcontacts
contacts = client.filter_contacts(field, operator, value)
# operator options: =, !=, IN, NIN, <, >, ~, !~, ^, $
```
#### - Create contact
```python
# role options are: 'user' and 'lead'
# signed_up_at and last_seen_at use epoch time stamp. For example: 1685986703 equals Monday, 5 June 2023 17:38:23
# custom_attributes dict structure:
#     {"field_name": "field_value", "field_name": "field_value", ...}
contact = client.create_contact(
    role: str, 
    email: str, 
    external_id: str = None,
    phone: str = None,
    name: str = None,
    avatar: str = None,
    signed_up_at: int = None,
    last_seen_at: int = None,
    owner_id: int = None,
    unsubscribed: bool = None,
    custom_attributes: dict = None
)
```
#### - Add tag to contact
```python
response = client.add_tag_to_contact(contact_id, tag_id)
```
#### - Create a note
```python
text = "this is a note"
response = client.create_note(contact_id, text)
```
