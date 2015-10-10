PROJECT="docpy"

test:
	py.test -s tests

test.report:
	coverage run --source $(PROJECT) -m py.test -s tests && coverage report

test.html:
	coverage run --source $(PROJECT) -m py.test -s tests && coverage html && open htmlcov/index.html
