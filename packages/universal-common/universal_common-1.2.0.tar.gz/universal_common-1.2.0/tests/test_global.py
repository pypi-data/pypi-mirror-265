from universal_common import coalesce, Dictionary, List, SqlConnectionStringBuilder, first, first_or_default, last, last_or_default

class TestGlobal:
    def test_coalesce_works(self):
        assert coalesce() is None
        assert coalesce(None, 1) == 1
        assert coalesce(2, 1) == 2
        assert coalesce(3) == 3
        assert coalesce(4, None) == 4

    def test_dictionary(self):
        dictionary: Dictionary = Dictionary({ "asdf": 1 })
        assert dictionary.asdf == 1
        assert dictionary["asdf"] == 1

        dictionary.b = 5
        assert dictionary.b == 5
        assert dictionary["b"] == 5

        assert dictionary.c is None

        del dictionary.b

        assert dictionary.b is None

    def test_list(self):
        list = List([1, 2, 5, 4])
        assert list.first() == 1
        assert list.first(lambda x: x > 3) == 5
        assert list.first_or_default() == 1
        assert list.first_or_default(lambda x: x > 3) == 5
        assert list.first_or_default(lambda x: x > 6) is None

    def test_linq_like(self):
        iterable = [1, 2, 5, 4]
        assert first(iterable) == 1
        assert first(iterable, lambda x: x > 3) == 5
        assert first_or_default(iterable) == 1
        assert first_or_default(iterable, lambda x: x > 3) == 5
        assert first_or_default(iterable, lambda x: x > 6) is None

    def test_sql_connection_string_builder(self):
        sql_connection_string_builder: SqlConnectionStringBuilder = SqlConnectionStringBuilder()
        sql_connection_string_builder.server = "Test"
        sql_connection_string_builder.database = "db"
        sql_connection_string_builder.user_id = "user1"
        sql_connection_string_builder.password = "pwd"

        assert str(sql_connection_string_builder) == "Server=Test;Database=db;Uid=user1;Pwd=pwd"