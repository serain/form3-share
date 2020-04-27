# form3-client

## Description

This is a client library for Form3's fake account [API service](https://github.com/form3tech-oss/interview-accountapi).

## Run Tests

```
$ docker-compose up
...
form3_client_1  | ----------- coverage: platform linux, python 3.7.7-final-0 -----------
form3_client_1  | Name                Stmts   Miss  Cover
form3_client_1  | ---------------------------------------
form3_client_1  | form3/__init__.py       3      0   100%
form3_client_1  | form3/account.py       30      0   100%
form3_client_1  | form3/baseapi.py       58      6    90%
form3_client_1  | form3/manager.py       15      0   100%
form3_client_1  | ---------------------------------------
form3_client_1  | TOTAL                 106      6    94%
form3_client_1  | 
form3_client_1  | 
form3_client_1  | ============================== 6 passed in 2.53s ===============================
```

## Example Usage

### List Accounts

```python
import form3
manager = form3.Manager()
accounts = manager.get_all_accounts()
```

### Get Account by ID

```python
import form3
manager = form3.Manager()
account = manager.get_account(account_id="11962ab6-ed03-4216-a88e-e94ffad552d2")
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
