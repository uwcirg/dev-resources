"""Module to anonymize all PHI fields in Tokens table """
import os
import yaml


def insert_token(cursor, token):
    # skip out if a match is found; simplifies development cycles
    cursor.execute("SELECT count(*) FROM tokens WHERE client_id='%s'" % token['client_id'])
    if cursor.fetchone()[0] == 1:
        return

    print("Inserting token '%s'" % token['name'])
    values = (
        token['client_id'], token['user_id'], token['token_type'],
        token['access_token'], token['expires'], token['_scopes'])
    insert_clause = (
        "INSERT INTO tokens (client_id, user_id, token_type, access_token, expires, _scopes) "
        "VALUES ('%s', %s, '%s', '%s', '%s', '%s')")

    cursor.execute(insert_clause % values)


def transform(cursor, custom_dir):
    # remove all tokens from prod; add back in one for dev/test Assessment Engine
    cursor.execute("DELETE FROM tokens")
    print(f"Deleted {cursor.rowcount} tokens rows")

    with open(os.path.join(custom_dir, "config.yaml"), 'r') as yamldata:
        for token in yaml.safe_load(yamldata)['tokens']:
            insert_token(cursor, token)
