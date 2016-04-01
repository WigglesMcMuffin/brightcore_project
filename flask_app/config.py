def get_database_uri(env=None):
	if env == 'prod':
		return '' #return postgres or some such
	elif env == 'testing':
		return 'sqlite:////code/tmp/test.db'
	else:
		return 'sqlite:////code/tmp/prod.db'