.PHONY: serve
serve:
	flask run

.PHONY: test
test:
	FLASK_ENV=testing coverage run -m pytest
