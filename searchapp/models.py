from django.db import models
import sqlite3


from django.db import models
from django.conf import settings

class Anime(models.Model):
    anime_id = models.IntegerField(null=True, blank=True) 
    name = models.CharField(max_length=255, null=True, blank=True)  
    genre = models.CharField(max_length=255, null=True, blank=True)  
    type = models.CharField(max_length=50, null=True, blank=True)  
    episodes = models.CharField(max_length=255,null=True, blank=True)  
    rating = models.CharField(max_length=255,null=True, blank=True)  
    members = models.CharField(max_length=255,null=True, blank=True)  
    image_url = models.CharField(max_length=1024, null=True, blank=True) 

class AnimeRating(models.Model):
    user_id = models.CharField(max_length=255, null=True, blank=True)  
    anime_id = models.CharField(max_length=255, null=True, blank=True) 
    rating = models.CharField(max_length=255,null=True, blank=True)
    

    


def db_connect(db_path):
    """Connect to the SQLite database."""
    conn = sqlite3.connect(db_path)
    return conn

def search_animes(conn, name=None, genre=None, anime_type=None,  sort="length_desc"):
    """Search animes based on name fragment, genre, and type."""

    query = "SELECT * FROM searchapp_anime WHERE genre NOT LIKE '%Hentai%' "  
    params = []

    # Append conditions based on provided arguments
    if name:
        query += " AND name LIKE ?"
        params.append(f'%{name}%')
    if genre:
        query += " AND genre LIKE ?"
        params.append(f'%{genre}%')
    if anime_type:
        query += " AND type = ?"
        params.append(anime_type)

    

    sort_options = {
        "length_asc": "episodes ASC",
        "length_desc": "episodes DESC",
        "rating_asc": "rating ASC",
        "rating_desc": "rating DESC"
    }
    sort_query = sort_options.get(sort, "rating DESC")  # Default sort
    query += f" ORDER BY {sort_query}"


    cursor = conn.cursor()
    cursor.execute(query, params)
    return fetch_results_as_dict(cursor)


def fetch_results_as_dict(cursor):
    """Fetch query results and convert them into a list of dictionaries."""
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]



db_path = 'db.sqlite3'  
conn = db_connect(db_path)

conn.close()


def get_random_anime(conn):
    """Fetch a random anime from the database."""
    query = "SELECT * FROM searchapp_anime WHERE rating > 8.5 AND genre NOT LIKE '%Hentai%' ORDER BY RANDOM() LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(query)
    # Use your existing function to convert the cursor to a dictionary
    result = fetch_results_as_dict(cursor)
    if result:
        return result[0]  # fetch_results_as_dict likely returns a list, so we take the first item
    return None



def match_user_to_cluster(request):
    user_ratings = request.session.get('ratings', {})
    max_score = -float('inf')
    best_cluster = None

    # Assume you have a function to load cluster profiles
    cluster_profiles = load_cluster_profiles()  # Implement this

    for cluster_id, profile in cluster_profiles.items():
        score = 0
        for anime_id, user_rating in user_ratings.items():
            cluster_rating = profile.get(anime_id, 0)  # Default to neutral if not rated
            # Update score based on user and cluster rating agreement
            if user_rating == 'good' and cluster_rating > 0:
                score += 1
            elif user_rating == 'bad' and cluster_rating < 0:
                score += 1
            # Add more conditions as needed
        
        if score > max_score:
            max_score = score
            best_cluster = cluster_id

    return best_cluster
