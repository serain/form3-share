# form3-client

## Description

This is a client library for Form3's fake account [API service](https://github.com/form3tech-oss/interview-accountapi).

## Run Tests

```
$ docker-compose up
...
form3_client_1  | ----------- coverage: platform linux, python 3.7.7-final-0 -----------
form3_client_1  | Name                  Stmts   Miss  Cover
form3_client_1  | -----------------------------------------
form3_client_1  | form3/__init__.py         3      0   100%
form3_client_1  | form3/account.py         33      0   100%
form3_client_1  | form3/httpclient.py      56      6    89%
form3_client_1  | form3/manager.py         16      0   100%
form3_client_1  | -----------------------------------------
form3_client_1  | TOTAL                   108      6    94%
form3_client_1  | 
form3_client_1  | 
form3_client_1  | ============================== 6 passed in 1.97s ===============================
```

## Example Usage

### Get all Accounts

```python
import form3
manager = form3.Manager()
accounts = manager.get_all_accounts()
for account in accounts:
    print(account)
```

### Get Account by ID

```python
import form3
manager = form3.Manager()
account = manager.get_account(account_id="11962ab6-ed03-4216-a88e-e94ffad552d2")
print(account)
```

### Create Account

```python
import form3
account = form3.Account(
    id="11962ab6-ed03-4216-a88e-e94ffad552d2",
    organisation_id="86b13a69-8cc9-40ba-940c-307d91743dbf",
    bank_id="400300",
    bank_id_code="GBDSC",
    base_currency="GBP",
    country="GB",
    bic="NWBKGB22",
)
account.create()
```

### Delete Account

```python
import form3
manager = form3.Manager()
account = manager.get_account(account_id="11962ab6-ed03-4216-a88e-e94ffad552d2")
account.delete()
```

## Technical Decisions

The [BaseAPI class](https://github.com/serain/form3-client/blob/master/form3/baseapi.py#L24) base class abstracts the HTTP layer by providing HTTP method helper functions and handling pagination. It is intended to be subclassed for each resource provided by the API (such as accounts).

[Account](https://github.com/serain/form3-client/blob/master/form3/account.py) subclasses BaseAPI and represents an Account resource. It provides methods for fetching, creating and deleting account resources.

The [Manager](https://github.com/serain/form3-client/blob/master/form3/manager.py#L6) class provides methods for fetching single accounts or listing of all accounts.

The API endpoint can be configured via the `API_ENDPOINT` environment variable.