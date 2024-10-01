"""Module to anonymize all PHI fields in ContactPoints table """


def transform(cursor, custom_dir):
    # remove any `value` fields, as some include user's phone numbers
    cursor.execute("UPDATE contact_points SET value = null WHERE value is not null")
    print(f"Updating {cursor.rowcount} contact_points rows")
