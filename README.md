# intercom-python
![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*intercom-python* is an API wrapper for intercom, written in Python.  
This library uses Oauth2 for authentication.
## Installing
```
pip install intercom-python
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