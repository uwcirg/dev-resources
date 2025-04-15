def transform(cursor, custom_dir):
    # remove clinician name from adherence data
    cursor.execute(
        "UPDATE adherence_data SET data = jsonb_set("
        "  data, '{clinician}', '\"redacted\"')"
    )
    print(f"Updating {cursor.rowcount} adherence_data rows for clinician name")

    # remove email identifier from adherence data
    sql = """
        WITH updated AS (
          SELECT
            id,
            jsonb_set(
              data,
              '{subject,identifier}',
              (
                SELECT jsonb_agg(
                  CASE
                    WHEN elem->>'system' = 'http://us.truenth.org/identity-codes/TrueNTH-username'
                    THEN jsonb_set(elem, '{value}', '"redacted"')
                    ELSE elem
                  END
                )
                FROM jsonb_array_elements(data->'subject'->'identifier') AS elem
              )
            ) AS new_data
          FROM research_data
          WHERE EXISTS (
            SELECT 1
            FROM jsonb_array_elements(data->'subject'->'identifier') AS elem
            WHERE elem->>'system' = 'http://us.truenth.org/identity-codes/TrueNTH-username'
          )
        )
        UPDATE research_data
        SET data = updated.new_data
        FROM updated
        WHERE research_data.id = updated.id;
        """
    cursor.execute(sql)
    print(f"Updating {cursor.rowcount} adherence_data rows for identifier")
