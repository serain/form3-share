import pytest
import os
import psycopg2


@pytest.fixture
def database_connection():
    dbhost = os.getenv("TEST_PSQL_HOST", "localhost")
    dbname = os.getenv("TEST_PSQL_DBNAME", "interview_accountapi")
    dbuser = os.getenv("TEST_PSQL_USER", "root")
    dbpass = os.getenv("TEST_PSQL_PASS", "password")
    with psycopg2.connect(
        dbname=dbname, host=dbhost, user=dbuser, password=dbpass
    ) as conn:
        yield conn


@pytest.fixture(scope="function")
def isolated_database_connection(database_connection):
    """
        Clear the test db before any tests.
        
        This is run before every test function using the fixture.
    """
    cur = database_connection.cursor()
    cur.execute('DELETE FROM "Account"')
    database_connection.commit()

    yield database_connection
