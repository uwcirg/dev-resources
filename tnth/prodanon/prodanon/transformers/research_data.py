def transform(cursor, custom_dir):
    # remove patient name from research data
    cursor.execute(
        "UPDATE research_data SET data = jsonb_set("
        "  data, '{encounter,patient,display}', '\"redacted\"')"
    )
    print(f"Updating {cursor.rowcount} research_data rows")
