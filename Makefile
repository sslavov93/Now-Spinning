.PHONY: devserver
devserver:
	flask run

.PHONY: test
test:
	FLASK_ENV=testing coverage run -m pytest

.PHONY: build
build:
	pyinstaller --onefile \
	--add-data 'now_spinning/__init__.py:now_spinning' \
	--add-data 'now_spinning/database.py:now_spinning' \
	--add-data 'now_spinning/models.py:now_spinning' \
	--add-data 'now_spinning/views.py:now_spinning' \
	--add-data 'now_spinning/templates:templates' \
	--add-data 'now_spinning/static:static' \
	--add-data 'config.json:.' \
	--icon=app.png server.py
