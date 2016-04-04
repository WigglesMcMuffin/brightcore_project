import os

def get_database_uri(env=None):
    if env == 'prod':
        return os.environ['DATABASE_URL']
    elif env == 'testing':
        return 'sqlite:////code/tmp/test.db'
    else:
        return 'sqlite:////code/tmp/dev.db'
