from __future__ import annotations
from .baseapi import BaseAPI


class Account(BaseAPI):
    def __init__(self, *args, **kwargs):
        # Only supporting a subset of all attributes listed, see docs for more
        # https://api-docs.form3.tech/api.html?shell#organisation-accounts-create
        self.id = None
        self.organisation_id = None
        self.version = 0
        self.bank_id = None
        self.bank_id_code = None
        self.base_currency = None
        self.bic = None
        self.country = None

        # The base class will load the values passed
        super().__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, account_id: str) -> Account:
        account = cls(id=account_id)
        account.load()
        return account

    def load(self) -> Account:
        """
            Fetch data about the account and populate object attributes.
        """
        data = self._get(f"organisation/accounts/{self.id}")

        self.id = data["id"]
        self.organisation_id = data["organisation_id"]
        self.version = int(data["version"])

        for key, value in data["attributes"].items():
            setattr(self, key, value)

        return self

    def create(self) -> None:
        """
            Create an Account.
        """
        payload = {
            "data": {
                "type": "accounts",
                "id": self.id,
                "organisation_id": self.organisation_id,
                "attributes": {
                    "country": self.country,
                    "base_currency": self.base_currency,
                    "bank_id": self.bank_id,
                    "bank_id_code": self.bank_id_code,
                    "bic": self.bic,
                },
            }
        }

        self._post("organisation/accounts", data=payload)

    def delete(self) -> bool:
        """
            Delete the account.

            Returns True if 204.
        """
        return self._delete(
            f"organisation/accounts/{self.id}", params={"version": int(self.version)}
        )
