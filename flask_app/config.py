def get_database_uri(env=None):
    if env == 'prod':
        return 'sqlite:////app/user/tmp/prod.db'
    elif env == 'testing':
        return 'sqlite:////code/tmp/test.db'
    else:
        return 'sqlite:////code/usr/tmp/dev.db'
