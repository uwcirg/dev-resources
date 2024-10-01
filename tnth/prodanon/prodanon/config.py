import os

class Config(object):
    db_host = os.environ.get("POSTGRES_HOST", '127.0.0.1')
    db_port = os.environ.get("POSTGRES_PORT", '5432')
    db_name = os.environ.get("POSTGRES_DB", "portaldb")
    db_user = os.environ.get("POSTGRES_USER", 'postgres')
    db_password = os.environ.get("POSTGRES_PASSWORD")

    @staticmethod
    def connection_args():
        return {
            "host": Config.db_host,
            "port": Config.db_port,
            "database": Config.db_name,
            "user": Config.db_user,
            "password": Config.db_password,
        }

    test_user_email = os.environ.get("TEST_USER_EMAIL", 'test@example.com')
