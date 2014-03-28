

TEST=test_conmongo.py

test:
	py.test $(TEST)

coverage:
	py.test --verbose --cov-report term-missing --cov=conmongo $(TEST)
