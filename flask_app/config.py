def get_database_uri(env=None):
    if env == 'prod':
        return ''  # return postgres or some such
    elif env == 'testing':
        return 'sqlite:////app/usr/tmp/test.db'
    else:
        return 'sqlite:////app/usr/tmp/prod.db'
