from __future__ import annotations
from typing import Optional

from .httpclient import HTTPClient


class Account:
    def __init__(
        self,
        id: str = None,
        organisation_id: Optional[str] = None,
        version: int = 0,
        bank_id: Optional[str] = None,
        bank_id_code: Optional[str] = None,
        base_currency: Optional[str] = None,
        bic: Optional[str] = None,
        country: Optional[str] = None,
        **kwargs,
    ):
        # Only supporting a subset of all attributes listed, see docs for more
        # https://api-docs.form3.tech/api.html?shell#organisation-accounts-create
        self.id = id
        self.organisation_id = organisation_id
        self.version = version
        self.bank_id = bank_id
        self.bank_id_code = bank_id_code
        self.base_currency = base_currency
        self.bic = bic
        self.country = country
        self._client = HTTPClient()

        # Support additional account properties
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_object(cls, account_id: str) -> Account:
        account = cls(id=account_id)
        account.load()
        return account

    def load(self) -> Account:
        """
            Fetch data about the account and populate object attributes.
        """
        data = self._client.get(f"organisation/accounts/{self.id}")

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

        self._client.post("organisation/accounts", data=payload)

    def delete(self) -> bool:
        """
            Delete the account.

            Returns True if 204.
        """
        return self._client.delete(
            f"organisation/accounts/{self.id}", params={"version": int(self.version)}
        )
