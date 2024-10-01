"""Module to anonymize all PHI fields in Users table"""
import os
import re
import yaml
from prodanon.config import Config

prefix_pattern = re.compile(r'^(__.*__)')


def email_for_user(id, current_email):
    """Generate a reasonable email address

    Needs to both anonymize and direct to an easy inbox for testing,
    as well as maintain prefixes with special meaning
    """
    test_user, test_domain = Config.test_user_email.split("@")
    email = f"{test_user}+{id}@{test_domain}"
    match = prefix_pattern.match(current_email)
    if match:
        email = match.group(0) + email
    return email


def transform(cursor, custom_dir):
    cursor.execute("SELECT id, email FROM users;")

    with open(os.path.join(custom_dir, "config.yaml"), 'r') as yamlfile:
        skip_ids = yaml.safe_load(yamlfile)['users']['preserve_ids']
    updates = []
    for id, em in cursor:
        if id in skip_ids:
            continue
        fname = f"{id}_fn"
        lname = f"{id}_ln"
        birthdate = "1950-01-01"
        email = email_for_user(id, em)

        updates.append(
            "UPDATE users SET"
            f" first_name = '{fname}',"
            f" last_name = '{lname}',"
            f" birthdate = '{birthdate}',"
            f" email = '{email}'"
            f" WHERE id = {id};"
        )

    print(f"Updating {len(updates)} user rows")
    for i in updates:
        cursor.execute(i)
