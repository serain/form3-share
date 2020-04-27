import os
import pytest
import uuid

import form3
from .basetest import BaseTest
from .test_account import create_account


class TestAccount(BaseTest):
    def setup_method(self):
        """
            Clear the test db before any tests.
        """
        cur = self.conn.cursor()
        cur.execute('DELETE FROM "Account"')
        self.conn.commit()

    def test_get_account(self):
        _id = "ff27e2aa-9605-4b4b-a0e5-3003ea9ccaaa"
        bank_id = "123456"

        create_account(id=_id, bank_id=bank_id)
        m = form3.Manager()
        account = m.get_account(account_id=_id)
        assert account.bank_id == bank_id

    def test_get_all_accounts(self):
        """
            Ensure we can get all accounts, tests pagination.
        """
        for _ in range(0, 110):
            _id = str(uuid.uuid4())
            create_account(id=_id)

        m = form3.Manager()
        accounts = m.get_all_accounts()

        assert len(accounts) == 110
