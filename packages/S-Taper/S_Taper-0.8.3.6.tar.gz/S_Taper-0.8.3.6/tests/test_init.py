import os

from s_taper import *
from s_taper.consts import *


def test_create_table():
    """
    Test the creation of a table in the database.
    """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT
    }
    table = Taper("test", 'test.db').create_table(scheme)
    assert "test.db" in os.listdir(".")
    os.remove("test.db")


def test_write():
    """
    Test the writing of data to a table.
    """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT
    }
    table = Taper("test", 'test.db').create_table(scheme)
    table.write([1, "name"])

    check = sqlite3.connect("test.db")
    check = check.cursor().execute("SELECT * FROM test").fetchall()
    assert (1, "name") in check
    os.remove("test.db")


def test_pickle_write():
    """
    Test the writing of data to a table.
    """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT,
        "pickle": TEXT
    }
    table = Taper("test", 'test.db').create_table(scheme)
    table.write([1, "name", {1, 2, 3}])

    check = sqlite3.connect("test.db")
    check = check.cursor().execute("SELECT * FROM test").fetchall()
    check = list(check[0])
    check[2] = pickle.loads(check[2])

    assert {1, 2, 3} in check

    os.remove("test.db")


def test_read():
    """
    Test the reading of data from a table.
    """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT
    }
    table = Taper("test", 'test.db').create_table(scheme)
    table.write([1, "name"])

    data = table.read("userid", 1)

    assert isinstance(data, s_taper.Taper._Answer)
    assert 1 in data and "name" in data  # Тест items

    os.remove("test.db")


def test_pickle_read():
    """
    Test the reading of data from a table.
    """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT,
        "pickle": TEXT
    }
    table = Taper("test", 'test.db').create_table(scheme)
    table.write([1, "name", [1, 2, 3]])

    data = table.read("userid", 1)

    assert isinstance(data, s_taper.Taper._Answer)
    assert 1 in data and "name" in data  # Тест items
    assert [1, 2, 3] in data  # Тест pickle

    os.remove("test.db")


def test_empty_read():
    """
    Test the reading of data from a table.
    """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT,
        "sleep": TEXT
    }
    table = Taper("test", 'test.db').create_table(scheme)
    table.write([1, "name", True])

    data = table.read("userid", 2)

    assert data == []
    os.remove("test.db")


def test_many_read():
    """
    Test the reading of data from a table.
    """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT,
        "sleep": BLN
    }
    table = Taper("test", 'test.db').create_table(scheme)
    table.write([1, "name1", True])
    table.write([2, "name2", True])
    table.write([3, "name3", False])
    table.write([4, "name4", False])

    data = table.read("sleep", False)

    assert len(data) == 2
    os.remove("test.db")


def test_many_pickle_read():
    """
    Test the reading of data from a table.
    """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT,
        "sleep": TEXT
    }
    table = Taper("test", 'test.db').create_table(scheme)
    table.write([1, "name", [True,]])
    table.write([2, "name1", [True,]])
    table.write([3, "name", [False,]])
    table.write([4, "name1", [False,]])

    data = table.read("name", "name")

    assert len(data) == 2
    assert [1, "name", [True,]] in data
    assert [3, "name", [False,]] in data

    os.remove("test.db")


def test_read_all():
    """
        Test the reading of data from a table.
        """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT,
        "sleep": BLN
    }
    table = Taper("test", 'test.db').create_table(scheme)
    table.write([1, "name1", True])
    table.write([2, "name2", True])
    table.write([3, "name3", False])
    table.write([4, "name4", False])


    data = table.read_all()
    print(data)
    assert len(data) == 4
    assert [1, "name1", True] in data
    assert [2, "name2", True] in data
    assert [3, "name3", False] in data
    assert [4, "name4", False] in data
    os.remove("test.db")


def test_read_pickle_all():
    """
        Test the reading of data from a table.
        """
    scheme = {
        "userid": INT + KEY,
        "name": TEXT,
        "sleep": TEXT
    }
    table = Taper("test", 'test.db').create_table(scheme)
    table.write([1, "name1", [True,]])
    table.write([2, "name2", [True,]])
    table.write([3, "name3", (False,)])
    table.write([4, "name4", {False}])


    data = table.read_all()

    assert len(data) == 4
    assert [1, "name1", [True,]] in data
    assert [2, "name2", [True,]] in data
    assert [3, "name3", (False,)] in data
    assert [4, "name4", {False}] in data
    os.remove("test.db")