test:
	`which django-admin.py` test --pythonpath=. --settings=assetfiles.tests.settings
coverage:
	`which django-admin.py` test --pythonpath=. --settings=assetfiles.tests.settings --with-coverage
