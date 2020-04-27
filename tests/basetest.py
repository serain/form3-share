import os
import psycopg2


class BaseTest:
    conn = None
    dbhost = os.getenv("TEST_PSQL_HOST", "localhost")
    dbname = os.getenv("TEST_PSQL_DBNAME", "interview_accountapi")
    dbuser = os.getenv("TEST_PSQL_USER", "root")
    dbpass = os.getenv("TEST_PSQL_PASS", "password")

    def setup_class(self):
        """
            Setup DB connection
        """
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            host=self.dbhost,
            user=self.dbuser,
            password=self.dbpass,
        )

    def teardown_class(self):
        """
            Wipe any residual test data and close DB connection
        """
        self.conn.close()
