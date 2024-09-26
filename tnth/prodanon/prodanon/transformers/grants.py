"""Module to anonymize all PHI fields in Grants table """


def transform(cursor, custom_dir):
    # remove all grants - wouldn't want them functioning on different system
    cursor.execute("DELETE FROM grants")
    print(f"Deleted {cursor.rowcount} grants rows")
