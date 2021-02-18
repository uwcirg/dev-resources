-- Create default unit test db and roles --

CREATE EXTENSION IF NOT EXISTS dblink;

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE  rolname = 'test_user') THEN

      CREATE ROLE test_user LOGIN PASSWORD '4tests_only';
   END IF;
END
$do$;

create database portal_unit_tests owner test_user;
DO
$do$
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = 'portal_unit_tests') THEN
      RAISE NOTICE 'Database already exists';  -- optional
   ELSE
      PERFORM dblink_exec('dbname=' || current_database()  -- current db
                        , 'CREATE DATABASE portal_unit_tests OWNER test_user');
   END IF;
END
$do$;
