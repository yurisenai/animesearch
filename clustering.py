import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

try:
    conn = sqlite3.connect('db.sqlite3')

    query = """
    SELECT user_id, anime_id, rating
    FROM searchapp_animerating
    """
    df = pd.read_sql_query(query, conn)

finally:
    conn.close()

# Force numeric values
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Replace -1 with NaN and drop rows with NaN
df['rating'] = df['rating'].replace(-1, np.nan)
df.dropna(subset=['rating'], inplace=True)

# Pivot the DataFrame to create a user-item matrix
ratings_matrix = df.pivot_table(index='user_id', columns='anime_id', values='rating')

# Fill missing values with the mean rating of each user
ratings_matrix_filled = ratings_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)

# Initialize and fit the KMeans model
kmeans = KMeans(n_clusters=10, random_state=42)
kmeans.fit(ratings_matrix_filled)

# Get the cluster labels for each user and add them to the dataframe
cluster_labels = kmeans.labels_
ratings_matrix_filled['cluster'] = cluster_labels

# Print out the first few rows of the ratings matrix to see the cluster assignments
print(ratings_matrix_filled.head())

# Calculate and print out the mean rating in each cluster for each anime
cluster_means = ratings_matrix_filled.groupby('cluster').mean()
print(cluster_means)

# Print information for each cluster
for i in range(10):  
    print(f"Cluster {i+1}:")
    print(f"Number of users: {sum(cluster_labels == i)}")
    # Additional statistics can be added here


# Assuming you have 10 clusters numbered from 0 to 9
number_of_clusters = 10

for cluster_index in range(number_of_clusters):
    # Filter the DataFrame for the current cluster
    cluster_data = ratings_matrix_filled[ratings_matrix_filled['cluster'] == cluster_index]
    
    # Drop the 'cluster' column to only have ratings
    cluster_data = cluster_data.drop(columns=['cluster'])
    
    # Calculate the mean rating for each anime in the cluster
    mean_ratings = cluster_data.mean().sort_values(ascending=False)
    

# Initialize an empty list to store data
top_anime_by_cluster = []

# Loop through each cluster
for cluster_index in range(number_of_clusters):
    # Filter the DataFrame for the current cluster
    cluster_data = ratings_matrix_filled[ratings_matrix_filled['cluster'] == cluster_index]
    
    # Drop the 'cluster' column to only have ratings
    cluster_data = cluster_data.drop(columns=['cluster'])
    
    # Calculate the mean rating for each anime in the cluster
    mean_ratings = cluster_data.mean().sort_values(ascending=False)
    
    # Select the top 21 anime
    top_21_anime = mean_ratings.head(21)
    
    # Append the top 21 anime with their ratings and cluster number to the list
    for anime_id, rating in top_21_anime.items():
        top_anime_by_cluster.append({
            "Cluster": cluster_index,
            "Anime ID": anime_id,
            "Average Rating": rating
        })

# Convert the list to a DataFrame
top_anime_by_cluster_df = pd.DataFrame(top_anime_by_cluster)

# Export the DataFrame to a CSV file
top_anime_by_cluster_df.to_csv('top_21_anime_by_cluster.csv', index=False)
