from typing import List
from .baseapi import BaseAPI
from .account import Account


class Manager(BaseAPI):
    def __init__(self):
        super().__init__()

    def get_all_accounts(self) -> List[Account]:
        """
            Returns a list of all Account objects.
        """
        data = self._get("organisation/accounts", params={"page[size]": 100})

        accounts = []
        for jsoned in data:
            account = Account(
                id=jsoned["id"],
                organisation_id=jsoned["organisation_id"],
                version=jsoned["version"],
                **jsoned["attributes"],
            )
            accounts.append(account)

        return accounts

    def get_account(self, account_id: str) -> Account:
        """
            Return an Account object given its ID.
        """
        return Account.get_object(account_id=account_id)
