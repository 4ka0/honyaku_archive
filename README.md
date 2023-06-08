# Honyaku Archive

A webapp for archiving and searching translations and glossaries.

You can do the following:
* Search the content of glossaries and translations.
* Upload glossaries from text files.
* Create, edit, and delete glossaries.
* Upload translations from tmx and docx files.
* Edit and delete translations.

## To download and run

* Clone this repo into a location of your choosing.<br>
`git clone https://github.com/4ka0/honyaku_archive.git`

* Move into the project folder.<br>
`cd honyaku_archive`

* Activate a virtual environment<br>
(Example using venv:)<br>
`python3 -m venv venv`<br>
`source venv/bin/activate`

* Install the dependencies.<br>
`pip install -r requirements.txt`

* Create a user.<br>
`python manage.py createsuperuser`

* Run the local server.<br>
`python manage.py runserver`

* Access "localhost:8000" in your browser.<br>

* Log in and start adding glossaries and translations.<br>

### Built using:

* Python 3.10
* Django 4.1.3
* Bootstrap 5

### Screenshots

Home page:</br></br>
<img src="screenshots/home.png"></br>

Glossary detail page:</br></br>
<img src="screenshots/glossary-detail.png"></br>

Translation detail page:</br></br>
<img src="screenshots/translation-detail.png"></br>

Search results:</br></br>
<img src="screenshots/search-results.png"></br>

Search options:</br></br>
<img src="screenshots/dropdown.png"></br>

Add glossary entry form:</br></br>
<img src="screenshots/add-entry.png"></br>

Upload glossary form:</br></br>
<img src="screenshots/glossary-upload.png"></br>

Upload translation form:</br></br>
<img src="screenshots/translation-upload.png"></br>
