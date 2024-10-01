"""Module to re-create dev specific clients

The prod-anon process brings over all prod specific data.  Clients is an exception
where the configured dev clients need to be preserved, to maintain integration
with other dev services

"""
import os
import yaml


def insert_client(cursor, client):
    # insert a client similar to the original dev/test values, for functional integration
    # with existing services (i.e. assessment engine or clients with long life tokens)

    # skip out if a match is found; simplifies development cycles
    cursor.execute("SELECT count(*) FROM clients WHERE client_id='%s'" % client['client_id'])
    if cursor.fetchone()[0] == 1:
        return

    print("Inserting client '%s'" % client['name'])
    values = (
        client['client_id'], client['client_secret'], client['user_id'], client['_redirect_uris'],
        client['_default_scopes'], client['callback_url'])
    insert_clause = (
        "INSERT INTO clients (client_id, client_secret, user_id, _redirect_uris, "
        "_default_scopes, callback_url) VALUES ('%s', '%s', %s, '%s', '%s', '%s')")

    cursor.execute(insert_clause % values)

    if client['intervention_name']:
        cursor.execute(
            "UPDATE interventions SET client_id = '%s' WHERE name = '%s'" %
            client['client_id'], client['intervention_name'])


def transform(cursor, custom_dir):
    """AE needs to point to the old dev version, as described in the custom/config.yaml"""
    # modify all existing prod client redirect uris to avoid any accidental interaction
    cursor.execute("SELECT client_id, _redirect_uris FROM clients ")
    updates = []
    for id, uri in cursor:
        updates.append((id, f"<disabled>{uri}"))
    print(f"Updating {len(updates)} client rows")
    for id, uri in updates:
        cursor.execute(f"UPDATE clients set _redirect_uris='{uri}' WHERE client_id='{id}'")

    with open(os.path.join(custom_dir, "config.yaml"), 'r') as yamldata:
        for client in yaml.safe_load(yamldata)['clients']:
            insert_client(cursor, client)
