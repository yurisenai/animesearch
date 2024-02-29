
# Quick-Start Guide
You should only have to run one command: python manage.py runserver
Afterwards in the terminal will paste the address of the website, typically: http://127.0.0.1:8000/ 
You can ctrl+click this link or copy and paste it to use the software. 

## Details
You can download the datasets from here:

 https://drive.google.com/drive/folders/12cp7HPun-KIxGo9aUXEDfwOur__Axhps?usp=sharing 

and add them to the base directory

The datasets used are from Kaggle.com, we use anime.csv and rating.csv. I will describe how you can access and scrape these using the same methods I did.
First, download the zip file “animesearch.zip” provided with this submission. Open the project in VSCode and verify that anime.csv and rating.csv are in the base directory. Next click into animesearch/searchapp/management/commands in order to verify that the two command files import_animes.py and import_rating.py are present. 
Now to set up the database (assuming the project is downloaded correctly, such as models) run this series of commands in the terminal:

	python manage.py makemigrations
	python manage.py migrate
	python import_animes
	python import_rating
    
Once you have run all these commands you can check “db.sqlite3” to see all the data is in the appropriate tables. 


