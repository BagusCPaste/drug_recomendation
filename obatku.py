import pandas as pd
import streamlit as st
from PIL import Image

# Load data rekomendasi yang sudah ada
data = pd.read_csv('recommendation_data.csv')

# Cetak info tentang struktur data
st.write("Info Struktur Data:")
st.write(data.info())

# Cetak 5 baris pertama dari data
st.write("Lima Baris Pertama dari Data:")
st.write(data.head())


def recommend(keyword):
    # Cetak data untuk memastikan kita mendapatkan kata kunci yang benar
    st.write("Data untuk Kata Kunci:", keyword)

    # Pisahkan kata kunci menjadi list
    keywords = keyword.lower().split()

    # Filter data berdasarkan kata kunci
    selected_data = data[data['condition'].str.lower(
    ).str.contains('|'.join(keywords))]

    st.write(selected_data)

    select = selected_data
    drug_count = select['drugName'].nunique()
    select['recommendation_score'] = select['recommendation_score'] / drug_count
    group_drug = select.groupby(['drugName']).agg(
        {'recommendation_score': ['sum']})
    group_drug = group_drug[('recommendation_score', 'sum')
                            ].sort_values(ascending=False)
    drug_score = dict(group_drug)
    recommendations = list(drug_score.keys())[:5] if len(
        drug_score) > 5 else list(drug_score.keys())
    return recommendations


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

if st.button("Rekomendasi"):
    # Panggil fungsi rekomendasi
    recommendations = recommend(user_keyword)

    # Tampilkan hasil rekomendasi
    st.markdown(
        f"<div style='border: 2px solid #DC143C; padding: 10px; border-radius: 10px; background-color: #FFE4E1; color: #DC143C;'>"
        f"<h3>Rekomendasi 5 Obat Terbaik untuk Kata Kunci {user_keyword.upper()}:</h3>"
        f"1. {recommendations[0]}<br>"
        f"2. {recommendations[1]}<br>"
        f"3. {recommendations[2]}<br>"
        f"4. {recommendations[3]}<br>"
        f"5. {recommendations[4]}<br>"
        f"</div>", unsafe_allow_html=True
    )
