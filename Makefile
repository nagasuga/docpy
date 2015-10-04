PROJECT="docpy"

test:
	py.test -s tests

report:
	coverage run --source $(PROJECT) -m py.test && coverage report

report.html:
	coverage run --source $(PROJECT) -m py.test && coverage html && open htmlcov/index.html
