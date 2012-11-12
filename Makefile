test:
	`which django-admin.py` test --pythonpath=. --settings=assetfiles.tests.settings assetfiles
coverage:
	coverage run --branch --source=assetfiles `which django-admin.py` test --pythonpath=. --settings=assetfiles.tests.settings assetfiles
	coverage report --omit=assetfiles/test*
