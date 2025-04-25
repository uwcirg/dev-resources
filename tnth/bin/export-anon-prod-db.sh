#!/bin/sh -e

cmdname="$(basename "$0")"
BACKUPS_DIR=/backups/truenth-portal

usage() {
    cat << USAGE >&2
Usage:
    $cmdname [-h]
    -h  Show this help message
    -o  Override default output location (/tmp)

    Generates a postgreSQL database dump of an anonymized version of
    the production database.  Obtains the source file from the most recent
    backup found in $BACKUPS_DIR

    The source file is imported into a temporary database, the 'proanon'
    process is run to clean it.  Subsequently exported to output as directed.

USAGE
    exit 1
}

while getopts "ho:" option; do
    case "${option}" in
        h)
            usage
	    ;;
        o)
	    output_dir="${OPTARG}"
	    ;;
        *)
            usage
	    ;;
    esac
done
shift $((OPTIND-1))

default_output_dir=/tmp
OUTPUT_DIR="${output_dir:-$default_output_dir}"

# Bring down any stale runs or volumes
echo "===\n= Purge previous prod anon containers and volumes\n===\n"
docker compose -f prod-anon.yaml down -v

echo "===\n= Bring up temporary database for transformation\n===\n"
# Bring up only the database layer during import
docker compose -f prod-anon.yaml up -d db_target

# Probably a better way to determine when Postgres layer is up...
sleep 10

SOURCE=$(ls -t "$BACKUPS_DIR" | head -n 1)
echo "===\n= Importing ${SOURCE} into temp db\n===\n"
docker compose -f prod-anon.yaml exec db_target bash -c "\
 if [[ ${SOURCE} == *.gz ]]; then \
   gunzip -c /tmp/backups/${SOURCE} | \
   psql --username postgres anonportaldb; \
 else \
   psql --username postgres anonportaldb -f /tmp/backups/${SOURCE}; \
  fi"


echo "===\n= Launch de-identification process\n===\n"
docker compose -f prod-anon.yaml up prodanon
if [ $? -ne 0 ]; then
    echo "ERROR: from `prodanon` process; can't continue"
    exit 1
fi

output_filename="scrubbed-$(date --iso-8601=seconds).sql"
echo "===\n= Export de-identified database to: ${OUTPUT_DIR}/${output_filename} \n===\n"
docker-compose -f prod-anon.yaml exec db_target bash -c '\
    pg_dump \
        --dbname anonportaldb \
        --no-acl \
        --no-owner \
        --username postgres \
        --encoding utf8 '\
> "${OUTPUT_DIR}/${output_filename}"

