.PHONY: serve
serve:
	flask run

.PHONY: test
test:
	coverage run -m pytest
