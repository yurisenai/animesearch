from pyexpat.errors import messages
from django.shortcuts import redirect, render
from searchapp.models import Anime , search_animes, db_connect, get_random_anime
from django.views.decorators.csrf import csrf_exempt
import requests
import pandas as pd


def get_anime_image_url(anime_name):
    # Encode the anime name for use in a URL
    encoded_name = requests.utils.quote(anime_name)
    
    # Use the Jikan API search endpoint
    search_url = f"https://api.jikan.moe/v4/anime?q={encoded_name}&limit=1"
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        data = response.json()

        # Check if there are any results
        if data['data']:
            # Return the URL of the main image of the first search result
            return data['data'][0]['images']['jpg']['image_url']
        else:
            return None
    except Exception as e:
        print(f"Error fetching image URL: {e}")
        return None


def search_results(request):
    # Initialize results to None
    results = None

    if request.method == "POST":
        name = request.POST.get('search', '')
        genre = request.POST.get('genre', '')
        anime_type = request.POST.get('type', '')
        sort = request.POST.get('sort', '')

        conn = db_connect('db.sqlite3')

        results = search_animes(conn, name, genre, anime_type, sort)
        
        conn.close()

        display_limit = 90  # Change this to control the number of results displayed
        results = results[:display_limit]

        for anime in results:
            if not anime.get('image_url'):  
                new_image_url = get_anime_image_url(anime['name'])
                anime['image_url'] = new_image_url
                Anime.objects.filter(name=anime['name']).update(image_url=new_image_url)
    return render(request, 'search_results.html', {'results': results})




def rate_anime(request):
    # Check if the user has finished rating and wants recommendations
    if request.GET.get('action') == 'recommend':
        user_ratings = request.session.get('ratings', [])
        user_cluster = determine_user_cluster(user_ratings)
        
        # Fetch the top 21 anime for the determined cluster
        df_clusters = pd.read_csv('top_21_anime_by_cluster.csv')
        top_anime_ids = df_clusters[df_clusters['Cluster'] == user_cluster]['Anime ID'][9:21].tolist()

        
        # Fetch anime details from the database
        recommendations = Anime.objects.filter(anime_id__in=top_anime_ids)
        context = {'recommendations': recommendations}
        for anime in recommendations:
            if not anime.image_url:
                new_image_url = get_anime_image_url(anime.name)
                anime.image_url = new_image_url
                anime.save()  # Save the updated anime object
        return render(request, 'rate_anime.html', context)

    if request.method == 'POST':
        # Process the rating submission
        anime_id = request.POST.get('anime_id')
        rating = request.POST.get('rating')  # 'good', 'bad', 'unknown'

        if 'ratings' not in request.session:
            request.session['ratings'] = []
        request.session['ratings'].append({'anime_id': anime_id, 'rating': rating})
        request.session.modified = True

        # Redirect to show a new anime or recommendations
        return redirect('rate_anime')

    # Connect to the database and get a random anime
    # Assuming db_connect and get_random_anime are defined elsewhere
    conn = db_connect('db.sqlite3')
    random_anime = get_random_anime(conn)
    conn.close()

    # Ensure there's an image for the anime
    if not random_anime.get('image_url'):
        new_image_url = get_anime_image_url(random_anime['name'])
        random_anime['image_url'] = new_image_url
        Anime.objects.filter(name=random_anime['name']).update(image_url=new_image_url)

    context = {'random_anime': random_anime}
    return render(request, 'rate_anime.html', context)



def indexView(request):
    return render(request, 'index.html')

def view_ratings(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'clear_ratings':
            if 'ratings' in request.session:
                del request.session['ratings']
            return redirect('view_ratings')

    ratings = request.session.get('ratings', [])
    context = {'ratings': ratings}
    return render(request, 'view_ratings.html', context)


def determine_user_cluster(user_ratings, csv_path='top_21_anime_by_cluster.csv'):
    # Load the cluster-anime mapping
    df_clusters = pd.read_csv(csv_path)
    
    # Initialize a dictionary to keep track of scores for each cluster
    cluster_scores = {i: 0 for i in range(10)}  # Assuming 10 clusters (0-9)
    
    # Process each user rating
    for rating in user_ratings:
        anime_id = int(rating['anime_id'])
        rating_value = rating['rating']
        
        # Find the cluster(s) that include the anime
        if anime_id in df_clusters['Anime ID'].values:
            clusters = df_clusters[df_clusters['Anime ID'] == anime_id]['Cluster']
            for cluster in clusters:
                # Update the score based on the rating
                if rating_value == 'good':
                    cluster_scores[cluster] += 1
                elif rating_value == 'bad':
                    cluster_scores[cluster] -= 1
                # 'unknown' ratings do not change the score
    
    # Find the cluster with the highest score
    best_cluster = max(cluster_scores, key=cluster_scores.get)
    return best_cluster
