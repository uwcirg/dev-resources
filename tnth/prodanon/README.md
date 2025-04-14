# Prod Anon

Given a copy of production data, anonymize for safe development and test use,
without the PHI.

## Export from Prod

Tools such as [backup-docker.sh](https://github.com/uwcirg/truenth-portal/blob/develop/bin/backup-docker.sh)
make exporting easy.  Note the directory used.  Assuming `/backups/truenth-portal` 
for subsequent steps.

## Prepare Temporary Database for Transformation 

Using a checkout of this project on a PHI safe system, start up the `target_db`

```bash
git clone git@github.com:uwcirg/dev-resources.git
cd dev-resources/tnth

# Edit the config to name users, clients and tokens to preserve
cp prodanon/prodanon/custom/config.yaml{.default,}

# NB the need to name which project yaml file to use, given multiple in this namespace

# If same workspace was used before, wipe the volume to ensure a fresh start
docker compose -f prod-anon.yaml down -v

# Bring up only the database layer
docker compose -f prod-anon.yaml up -d db_target
```

## Import Production Data

Execute the backup script on the prod server (optional, can just use latest):

```bash
sudo /srv/www/eproms.truenth.org/truenth-portal/bin/backup-docker.sh -b /backups/truenth-portal
```

Import the most recent dump file from the backup directory:

```bash
SOURCE=$(ls -t /backups/truenth-portal | head -n 1)
docker compose -f prod-anon.yaml exec db_target bash -c "\
 if [[ ${SOURCE} == *.gz ]]; then \
   gunzip -c /tmp/backups/${SOURCE} | \
   psql --username postgres anonportaldb; \
 else \
   psql --username postgres anonportaldb -f /tmp/backups/${SOURCE}; \
  fi"
```

## Run the `prodanon` Transformation

Bring the service up in the foreground to wait (several minutes) for its conclusion.
```bash
docker compose -f prod-anon.yaml up prodanon
```

## Export the Transformed Database

```bash
docker-compose -f prod-anon.yaml exec db_target bash -c '\
    pg_dump \
        --dbname anonportaldb \
        --no-acl \
        --no-owner \
        --username postgres \
        --encoding utf8 '\
> scrubbed.sql
```

## Move export to target system, and import

```bash
scp scrubbed.sql $DEST:/tmp
ssh $DEST
cd /srv/www/hostpath/portal/docker

# potentially backup existing data first...
sudo ../bin/backup-docker.sh -b /backups/truenth-portal

# purge and recreate the database shell
../bin/restore-database.sh /tmp/scrubbed.sql

# restore the service
docker compose up -d
```
