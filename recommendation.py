# TASK 4: Movie Recommendation System
# CodSoft AI Internship
# Uses Content-Based Filtering + Collaborative Filtering (simple version)

# Install required library: pip install pandas numpy

import pandas as pd
import numpy as np

# ─────────────────────────────────────────
# DATASET: Movies with genres and ratings
# ─────────────────────────────────────────

movies_data = {
    'movie_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                 11, 12, 13, 14, 15],
    'title': [
        'The Dark Knight', 'Inception', 'Interstellar', 'The Matrix',
        'Avengers: Endgame', 'Iron Man', 'The Godfather', 'Pulp Fiction',
        'Forrest Gump', 'The Lion King', 'Toy Story', 'Finding Nemo',
        'The Shawshank Redemption', 'Goodfellas', 'Schindler\'s List'
    ],
    'genre': [
        'Action Crime', 'Action Sci-Fi Thriller', 'Sci-Fi Drama',
        'Action Sci-Fi', 'Action Sci-Fi', 'Action Sci-Fi',
        'Crime Drama', 'Crime Drama Thriller', 'Drama Romance',
        'Animation Adventure', 'Animation Adventure Comedy',
        'Animation Adventure', 'Drama', 'Crime Drama', 'Drama History'
    ],
    'rating': [9.0, 8.8, 8.6, 8.7, 8.4, 7.9, 9.2, 8.9, 8.8, 8.5,
               8.3, 8.1, 9.3, 8.7, 8.9]
}

# User ratings dataset (simulated)
ratings_data = {
    'user_id': [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4],
    'movie_id': [1,2,3,5,2,4,6,10,7,8,13,14,9,10,11,12],
    'user_rating': [5,4,5,3,5,4,4,3,5,5,5,4,4,3,5,4]
}

movies_df = pd.DataFrame(movies_data)
ratings_df = pd.DataFrame(ratings_data)


# ─────────────────────────────────────────
# METHOD 1: CONTENT-BASED FILTERING
# ─────────────────────────────────────────

def content_based_recommend(movie_title, top_n=5):
    """
    Recommend movies similar to the given movie based on genre.
    Uses simple word overlap (Jaccard similarity).
    """
    movie_title = movie_title.strip().lower()

    # Find the movie
    match = movies_df[movies_df['title'].str.lower() == movie_title]
    if match.empty:
        print(f"\n❌ Movie '{movie_title}' not found in database.")
        print("Available movies:")
        for title in movies_df['title']:
            print(f"  - {title}")
        return

    target = match.iloc[0]
    target_genres = set(target['genre'].lower().split())

    similarities = []
    for _, row in movies_df.iterrows():
        if row['movie_id'] == target['movie_id']:
            continue
        row_genres = set(row['genre'].lower().split())
        # Jaccard similarity
        intersection = len(target_genres & row_genres)
        union = len(target_genres | row_genres)
        similarity = intersection / union if union > 0 else 0
        similarities.append((row['title'], similarity, row['rating']))

    # Sort by similarity, then by rating
    similarities.sort(key=lambda x: (x[1], x[2]), reverse=True)

    print(f"\n🎬 Because you liked '{target['title']}', you might enjoy:")
    print("-" * 50)
    for i, (title, sim, rating) in enumerate(similarities[:top_n], 1):
        print(f"  {i}. {title}  (Rating: {rating}/10)")
    print()


# ─────────────────────────────────────────
# METHOD 2: COLLABORATIVE FILTERING
# ─────────────────────────────────────────

def collaborative_recommend(user_id, top_n=5):
    """
    Recommend movies based on what similar users liked.
    Uses user-user collaborative filtering.
    """
    # Build user-movie matrix
    user_movie_matrix = ratings_df.pivot_table(
        index='user_id', columns='movie_id', values='user_rating'
    ).fillna(0)

    if user_id not in user_movie_matrix.index:
        print(f"\n❌ User {user_id} not found. Available users: {list(user_movie_matrix.index)}")
        return

    # Calculate cosine similarity between users
    def cosine_similarity(u1, u2):
        dot = np.dot(u1, u2)
        norm = np.linalg.norm(u1) * np.linalg.norm(u2)
        return dot / norm if norm > 0 else 0

    target_user = user_movie_matrix.loc[user_id].values
    similarities = {}

    for uid in user_movie_matrix.index:
        if uid == user_id:
            continue
        sim = cosine_similarity(target_user, user_movie_matrix.loc[uid].values)
        similarities[uid] = sim

    # Find movies rated by similar users but not by target user
    target_watched = set(ratings_df[ratings_df['user_id'] == user_id]['movie_id'])
    recommendations = {}

    for uid, sim in similarities.items():
        user_ratings = ratings_df[ratings_df['user_id'] == uid]
        for _, row in user_ratings.iterrows():
            mid = row['movie_id']
            if mid not in target_watched:
                if mid not in recommendations:
                    recommendations[mid] = 0
                recommendations[mid] += sim * row['user_rating']

    if not recommendations:
        print(f"\n❌ Not enough data to make recommendations for User {user_id}.")
        return

    # Sort and display
    sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

    print(f"\n👤 Recommendations for User {user_id} (Collaborative Filtering):")
    print("-" * 50)
    for i, (mid, score) in enumerate(sorted_recs[:top_n], 1):
        title = movies_df[movies_df['movie_id'] == mid]['title'].values[0]
        rating = movies_df[movies_df['movie_id'] == mid]['rating'].values[0]
        print(f"  {i}. {title}  (Rating: {rating}/10)")
    print()


# ─────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────

def main():
    print("=" * 55)
    print("   🎬 CodSoft Movie Recommendation System")
    print("=" * 55)

    while True:
        print("\nChoose recommendation type:")
        print("  1. Content-Based (by movie similarity)")
        print("  2. Collaborative Filtering (by user similarity)")
        print("  3. Show all movies")
        print("  4. Exit")

        choice = input("\nEnter choice (1/2/3/4): ").strip()

        if choice == '1':
            movie = input("Enter a movie you liked: ").strip()
            content_based_recommend(movie)

        elif choice == '2':
            try:
                uid = int(input("Enter your user ID (1-4): ").strip())
                collaborative_recommend(uid)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '3':
            print("\n📽️  Available Movies:")
            print("-" * 50)
            for _, row in movies_df.iterrows():
                print(f"  {row['movie_id']:>2}. {row['title']:<35} | Rating: {row['rating']}/10")

        elif choice == '4':
            print("\nThank you for using the Recommendation System! Goodbye! 👋")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()