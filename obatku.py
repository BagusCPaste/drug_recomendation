import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import regex as re

# Load data rekomendasi yang sudah ada
data = pd.read_csv('recommendation_data.csv')

vectorizer = TfidfVectorizer()
X_new = vectorizer.fit_transform([x.lower() for x in data['full_konteks']])

kolom_tampil = ['drugName', 'condition', 'review',
                'recommendation_score']

# Cetak info tentang struktur data
st.header("Rekomendasi Obat Berdasarkan Review")

# Cetak 5 baris pertama dari data
st.write("Rekomendasi obat diberikan sesuai dengan hasil review yang ada dan direkomendasikan berdasarkan seberapa sering obat tersebut dikonsumsi.")
st.write(data[kolom_tampil].sort_values(
    by='recommendation_score', ascending=False))
st.write('---')


def searching(word):
    # match everyting that's not alphabet and digit and remove it
    word = re.sub('[^a-zA-Z0-9 ]', '', word.lower())
    query_vec = vectorizer.transform([word])
    similarity = cosine_similarity(query_vec, X_new).flatten()

    filtered = np.where(similarity != 0)[0]
    indices = np.argsort(-similarity[filtered])
    correct_indices = filtered[indices]
    result = data.iloc[correct_indices]

    if not len(result):
        return 'Result not found'

    overall = result['recommendation_score'] * similarity[correct_indices]

    return result.loc[overall.sort_values(ascending=False).index]


def recommend(keyword):
    # Cetak data untuk memastikan kita mendapatkan kata kunci yang benar
    st.write("Masukkan kondisi penyakit anda", keyword)

    data = searching(keyword)
    # st.write(selected_data)

    select = data
    drug_count = select['drugName'].nunique()
    select['recommendation_score'] = select['recommendation_score'] / drug_count
    group_drug = select.groupby(['drugName']).agg(
        {'recommendation_score': ['sum']})
    group_drug = group_drug[('recommendation_score', 'sum')
                            ].sort_values(ascending=False)
    drug_score = dict(group_drug)
    recommendations = list(drug_score.keys())[:5] if len(
        drug_score) > 5 else list(drug_score.keys())

    return recommendations, data


# Tampilan aplikasi Streamlit
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #DC143C;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Aplikasi Rekomendasi Obat Berdasarkan Kondisi")

# Input kata kunci dari pengguna
user_keyword = st.text_input("Masukkan kata kunci kondisi Anda:")

# Menyembunyikan teks "Masukkan kata kunci kondisi Anda:" dan tetap mempertahankan kolom input
hide_streamlit_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if st.button("Cari Rekomendasi"):
    # Panggil fungsi rekomendasi
    recommendations, selected_data = recommend(user_keyword)

    # Tampilkan hasil rekomendasi
    st.markdown(
        f"<div style='border: 2px solid #DC143C; padding: 10px; border-radius: 10px; background-color: #FFE4E1; color: #DC143C;'>"
        f"<h3>Rekomendasi 5 obat untuk keluhan anda : </h3>"
        f"1. {recommendations[0].capitalize()}<br>"
        f"2. {recommendations[1].capitalize()}<br>"
        f"3. {recommendations[2].capitalize()}<br>"
        f"4. {recommendations[3].capitalize()}<br>"
        f"5. {recommendations[4].capitalize()}<br>"
        f"</div>", unsafe_allow_html=True
    )

    st.write(selected_data[kolom_tampil].sort_values(
        by='recommendation_score', ascending=False))
