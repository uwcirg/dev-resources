# CIRG Developer Resources

Intended to house utilities, shortcuts and tools likely to span projects.

## keygen

### Create a virtual environment for creating keys for config files (must be done once)

```
python3 -m venv venv
```
### Activate said environment (must be done on new shell or session)
```
source venv/bin/activate
```

### Install dependencies (must be done anytime requirements change)
```
pip install -r requirements.txt
```

### Run to generate the necessary keycloak keys from default file
```
keygen/populate_keys.py <path_to_default_config> --ouput <path_to_desired_config>
```

### Testing
```
pip install -r requirements.dev.txt
py.test keygen/tests.py
```


## tnth

### Copy the template files and edit as necessary.

```
cp default.env .env
```

### Start Services

```
docker-compose up --detach
```

### Reset database

For clean slate, stop the service and remove the volume, then restart: 

```
docker-compose down
docker volume ls
docker volume rm <volume_name>
docker-compose up --detach
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

