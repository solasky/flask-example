

### Quick start ###
visit http://flask.pocoo.org/ and follow the tutorial

Install python packages
```
$ sudo apt-get install python3-dev virtualenv g++
$ virtualenv -ppython3 venv; venv/bin/pip install -r requirements.txt
```

Start the server
```
$ venv/bin/python wsgi.py
```
server should start at http://localhost:8080/


Flask follows MVC model. 
* See webapp/__init__.py for the main file
* See webapp/views/examples.py for other routes
* See templates/*html for the html template files

Two (html serving) urls are valid here:
* http://localhost:8080/index.html
* http://localhost:8080/example_input.html

on /example_input.html, see how the input interacts with route in views/examples.py. Special focus on JSON/AJAX input.

### Exercise ###
* A Sqlite database is included in data/test.sqlite.
* Modify the package such that the functionalities implied on index.html are working
** Load data from data/test.sqlite, content_classification_tasktable
** sort, display, ordering and paging functions are working properly




