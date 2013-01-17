test:
	`which django-admin.py` test --pythonpath=. --settings=assetfiles.tests.settings --with-xunit -s
coverage:
	`which django-admin.py` test --pythonpath=. --settings=assetfiles.tests.settings --with-coverage --cover-package=assetfiles --cover-min-percentage=50
