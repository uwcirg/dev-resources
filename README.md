# CIRG Developer Resources

Intended to house utilities, shortcuts and tools likely to span projects.

## tnth

### Copy the template files and edit as necessary.

```
cp default.env .env
```

### Start Services

```
sudo docker-compose up --detach
```

### Reset database

For clean slate, stop the service and remove the volume, then restart: 

```
sudo docker-compose down
docker volume ls
docker volume rm <volume_name>
sudo docker-compose up --detach
```

### Import database

Example to import content from ``eproms-test`` system.  Set environment
variables to match configuration, defaults in `system-services.yaml`:

```
export PGUSER=postgres
export PGDATABASE=portaldb
export PGPASSWORD=redacted
export PGHOST=localhost
```

confirm naked `psql` functions, then execute import from named host:

```
HOST=eproms-test.cirg.washington.edu
ssh $HOST pgdump-${HOST} | psql --dbname $PGDATABASE
```

