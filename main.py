import pandas as pd
import streamlit as st
from PIL import Image

df = pd.read_csv('data/netflix_titles.csv')
df.dropna(subset=['title', 'listed_in', 'description'], inplace=True)
df = df[~df['type'].str.contains("TV Show")]
df['listed_in'] = df['listed_in'].str.split(', ')

genre_options = {
    '🎬 Action': 'Action & Adventure',
    '🎭 Drama': 'Dramas',
    '😂 Comedy': 'Comedies',
    '🌎 International TV Shows': 'International Movies',
    '🔍 Documentary': 'Documentaries',
    '🎤 Music': 'Music & Musicals',
    '🖤 Horror': 'Horror Movies',
    '🏆 Sci-Fi': 'Sci-Fi & Fantasy',
}


def recommend_movies(df, genre, num_recommendations=5):
    filtered_df = df[df['listed_in'].apply(lambda x: genre in x)]
    if filtered_df.empty:
        return None
    recommendations = filtered_df.sample(num_recommendations)
    return recommendations[['title', 'release_year', 'rating', 'description']]


def main():
    st.set_page_config(page_title="Netflix Movie Recommendation System", layout="wide")

    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f5;
            font-family: 'Arial', sans-serif;
        }
        .header {
            text-align: center;
            color: #e50914;
        }
        .recommendation {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .button-container {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .netflix-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #e50914;
            border: none;
            border-radius: 4px;
            text-align: center;
            cursor: pointer;
            text-decoration: none;
        }
        .netflix-button:hover {
            background-color: #f6123d;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Netflix Movie Recommendation System", anchor=None)
    st.markdown("<h2 class='header'>Explore the genres and get recommendations!</h2>", unsafe_allow_html=True)

    genre = st.selectbox("Select a genre:", list(genre_options.keys()), key="genre_select")

    if st.button("Recommend"):
        recommendations = recommend_movies(df, genre_options[genre])

        if recommendations is not None:
            st.write("Here are some movie recommendations for you:")
            for index, row in recommendations.iterrows():
                st.markdown(f"<div class='recommendation'>", unsafe_allow_html=True)
                st.write(f"**Title:** {row['title']}")
                st.write(f"**Release Year:** {row['release_year']}")
                st.write(f"**Rating:** {row['rating']}")
                st.write(f"**Description:** {row['description']}")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.write("No recommendations found for this genre. Please try another genre.")

    # Display Netflix logo beside the button
    netflix_logo = Image.open(r"C:\Users\TRIDEEP\Downloads\Python folder for idse course\Pycharm\Netflix_Symbol.png")
    st.image(netflix_logo, width=50)

    st.markdown(
        """
        <div class="button-container">
            <a class='netflix-button' href='https://www.netflix.com' target='_blank'>Visit Netflix</a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
