import os
import pytest

import form3


def create_account(**kwargs):
    """
        Helper to create an account with custom or default attributes.
    """
    account = form3.Account(
        id=kwargs.get("id", "11962ab6-ed03-4216-a88e-e94ffad552d2"),
        organisation_id=kwargs.get(
            "organisation_id", "86b13a69-8cc9-40ba-940c-307d91743dbf"
        ),
        bank_id=kwargs.get("bank_id", "400300"),
        bank_id_code=kwargs.get("bank_id_code", "GBDSC"),
        base_currency=kwargs.get("base_currency", "GBP"),
        country=kwargs.get("country", "GB"),
        bic=kwargs.get("bic", "NWBKGB22"),
    )
    account.create()

    return account


@pytest.mark.usefixtures("isolated_database_connection")
class TestAccount:
    def test_create_account(self):
        """
            Ensure we can create an account without raising any errors.
        """
        try:
            create_account()
        except Exception as e:
            pytest.fail(e)

    def test_load_account(self):
        """
            Ensure we can load an existing account from an account ID.
        """
        _id = "11962ab6-ed03-4216-a88e-e94ffad552d2"
        bank_id = "123456"

        create_account(id=_id, bank_id=bank_id)
        account = form3.Account(id=_id)
        account.load()

        assert account.bank_id == bank_id

    def test_delete_account(self):
        """
            Ensure an accounts doesn't exist anymore after we've deleted it.
        """
        _id = "11962ab6-ed03-4216-a88e-e94ffad552d2"
        account = create_account(id=_id)
        account.delete()

        with pytest.raises(form3.NotFoundError):
            form3.Account(id=_id).load()

    def test_get_account(self):
        """
            Ensure we can get an account from an account ID.
        """
        _id = "11962ab6-ed03-4216-a88e-e94ffad552d2"
        bank_id = "123456"

        create_account(id=_id, bank_id=bank_id)
        account = form3.Account.get_object(account_id=_id)

        assert account.bank_id == bank_id
