# Keep this file separate

# Usage:
# import hidden
# secrets = hidden.pg_secrets()


# psql -h host.com -p 5432 -U database user
# ---> Change dict values to match your credentials
# The default PostgreSQL port is 5432
def pg_secrets():
    return {
        "host": "host.com",
        "port": 5432,
        "database": "database",
        "user": "user",
        "pass": "pw"
    }


def psycopg2(secrets):
    """
    Return a psycopg2 connection string.
    'dbname=database user=user password=pw host=host.com port=5432'
    """
    return ('dbname='+secrets['database']+' user='+secrets['user']+
        ' password='+secrets['pass']+' host='+secrets['host']+
        ' port='+str(secrets['port']))