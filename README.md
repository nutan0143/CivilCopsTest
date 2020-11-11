### *Tool , Technologies and Version*

Python
Django
Djongo
MongoDB


### *Step for setup and Run the file*

1. Make folder
	
		mkdir folder_name

2. Go to folder
	
		cd folder_name

2. Clone code from github 

		git clone -b main https://github.com/nutan0143/CivilCopsTest.git

3. Make environemt

		virtualenv env

4. Activate environment

		a. env\Script\activate # for window

		b. source env/bin/activate #for mac and ubuntu

5. Install all requirement

		pip install -r requirements.txt

6. Migrate Your Project

		python manage.py migrate

7. Run project

		python manage.py runserver

