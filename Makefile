venv:
	virtualenv -p python3.6 venv
	./venv/bin/pip install -r requirements.txt

runserver: /usr/local/bin/docker-compose
	docker-compose run -p 8000:8000 django python ./src/manage.py runserver 0.0.0.0:8000

shell: /usr/local/bin/docker-compose
	docker-compose run django python ./src/manage.py shell

test:
	 docker-compose run django py.test -s ./src
