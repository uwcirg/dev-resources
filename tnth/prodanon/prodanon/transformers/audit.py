"""Module to anonymize all PHI fields in Audit table

Audit records fit into clean `context` buckets.  Most are benign, but a few
need cleanup.

'access': clean
'account': has a few `registered invited user %` with PHI
'assessment': clean
'authentication': has a few `Failed identity challenge %` with PHI
'consent': clean
'eproms': clean
'intervention': clean
'login': clean
'observation': clean
'organization': clean
'other': clean
'postgres': clean
'procedure': clean
'role': clean
'tou': clean
'user': tons of PHI - redact all comments.  Could be more selective if testing needs warrant.
"""
def transform(cursor, custom_dir):
    cursor.execute(
        "SELECT id, context, comment FROM audit "
        "WHERE context in ('account', 'authentication', 'user');")
    updates = []

    for id, context, comment in cursor:
        if context == 'account':
            if comment.startswith('registered invited user'):
                updates.append((id, "registered invited user <redacted>"))
        if context == 'authentication':
            if comment.startswith('Failed identity challenge'):
                updates.append((id, "Failed identity challenge <redacted>"))
        if context == 'user':
            updates.append((id, "<redacted>"))

    print(f"Updating {len(updates)} audit rows")
    for id, comment in updates:
        cursor.execute(f"UPDATE audit set comment='{comment}' WHERE id={id}")
