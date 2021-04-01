"""Pytest/Unittest Fixtures."""


class MockSnowflakeConnection(object):
    """Mock Connection object for Snowflake Connector."""

    @staticmethod
    def cursor():
        """Mock cursor function."""
        return MockSnowflakeCursor()


class MockSnowflakeCursor(object):
    """Mock Cursor object for Snowflake Cursor."""

    @staticmethod
    def executemany(query: str = None, params: tuple = None):
        """Mock executemany function."""
        return f"Executed query: {query}: {params}!"

    @staticmethod
    def close():
        """Mock close function."""
        return None
