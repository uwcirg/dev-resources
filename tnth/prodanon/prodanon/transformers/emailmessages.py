"""Module to anonymize all PHI fields in email_messages table

Might be nice to track recipients, for now purge.  (could track emails before obfuscation)

Sender includes email addresses of staff.  Purged.

The body of the emails are generally clean, except for introductions including names. Purged
at this time.

"""
def transform(cursor, custom_dir):
    cursor.execute(
        "UPDATE email_messages SET recipients = '<redacted>', sender = '<redacted>', "
        "body = '<redacted>'")
    print(f"Updating {cursor.rowcount} email_messages rows")
