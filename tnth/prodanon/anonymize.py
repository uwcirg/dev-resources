import importlib
import os
from prodanon.conn import Conn

def test_connection(cursor):
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    if not version[0].startswith('PostgreSQL '):
        raise RuntimeError("Unable to connect to PostgreSQL; Can't continue")


package = "prodanon"
transformers_dir = os.path.join(os.path.dirname(__file__), package, "transformers")
custom_dir = os.path.join(os.path.dirname(__file__), package, "custom")

if __name__ == '__main__':
    print("Begin Anonymize Data")

    transformers = [
        f[:-3] for f in os.listdir(transformers_dir) if f.endswith(".py") and f != "__init__.py"]
    with Conn() as cursor:
        test_connection(cursor)

        for transformer_module in transformers:
            module_path = f"{package}.transformers.{transformer_module}"
            module = importlib.import_module(module_path)
            if not hasattr(module, "transform"):
                raise ValueError(f"expected `transform()` function not found in {module_path}")
            print(f"Calling `{transformer_module}.transform()`")
            module.transform(cursor, custom_dir)

    print("Anonymize Data Complete")
