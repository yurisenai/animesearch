
# Quick-Start Guide
You can download the datasets from here:

 https://drive.google.com/drive/folders/12cp7HPun-KIxGo9aUXEDfwOur__Axhps?usp=sharing 

and add them to the base directory

You should only have to run one command: python manage.py runserver
Afterwards in the terminal will paste the address of the website, typically: http://127.0.0.1:8000/ 
You can ctrl+click this link or copy and paste it to use the software. 

## Details
To work with the data yourself: 
The datasets used are from Kaggle.com, we use anime.csv and rating.csv in any of the top projects if you search anime recommendation. I will describe how you can access and scrape these using the same methods I did.
Now to set up the database run this series of commands in the terminal:

	python manage.py makemigrations
	python manage.py migrate
	python import_animes
	python import_rating
	python clustering
    
Once you have run all these commands you can check “db.sqlite3” to see all the data is in the appropriate tables. 


