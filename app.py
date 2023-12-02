# import module
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly_express as px
import time
import plotly.graph_objects as go

st.set_page_config(
    page_title="Hajar Aswad",
    page_icon=":tada:",
    layout="wide",
)


st.header("GLOBAL PEACE")
st.text("by Hajar Aswad")

st.write("---")

image = Image.open('./image/peace.jpg')
st.image(image, use_column_width=True, width=1000)

st.write('----------')

datSet = pd.read_csv("dataset/clean.csv")

st.write("")

st.subheader("Diagram & Alert System")
st.text("oleh HAJAR ASWAD")

# Pilihan menu utama
menu_options = ["Diagram Pie Keamanan Dunia", "Alert System"]
selected_menu = st.radio("Pilih Menu:", menu_options)

# Jika memilih "Diagram Pie Keamanan Dunia"
if selected_menu == "Diagram Pie Keamanan Dunia":
    # Subjudul untuk bagian data grafik
    st.text("Data Grafik")

    # Menampilkan pilihan kolom untuk diagram pie
    selected_year = st.selectbox("Pilih Tahun:", ['Semua Tahun'] + list(datSet['year'].unique()))
      # Urutkan negara secara alfabetis
    countries_sorted = sorted(datSet['Country'].unique())
    selected_country = st.selectbox("Pilih Negara:", ['Semua Negara'] + countries_sorted)

    # Memfilter data berdasarkan tahun dan negara yang dipilih
    if selected_year == 'Semua Tahun' and selected_country == 'Semua Negara':
        filtered_data = datSet
    elif selected_year == 'Semua Tahun':
        filtered_data = datSet[datSet['Country'] == selected_country]
    elif selected_country == 'Semua Negara':
        filtered_data = datSet[datSet['year'] == selected_year]
    else:
        filtered_data = datSet[(datSet['year'] == selected_year) & (datSet['Country'] == selected_country)]

    # Menampilkan diagram pie untuk kolom-kolom tertentu
    if not filtered_data.empty:
        labels = ['Safety and Security', 'Ongoing Conflict', 'Militarian']
        values = [filtered_data[label].sum() for label in labels]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])  # Mengatur hole untuk memberi ruang untuk keterangan

        # Menambahkan teks keterangan
        if 'Condition' in filtered_data.columns:  # Memeriksa apakah kolom 'Condition' ada dalam dataset
            if selected_country == 'Semua Negara':
                condition_text = '-'
            else:
                condition_text = filtered_data['Condition'].iloc[0]

            fig.add_annotation(
                go.layout.Annotation(
                    text=f'Condition: {condition_text}',
                    showarrow=False,
                    x=0.5,
                    y=0.5,
                    font=dict(size=11),
                )
            )
        else:
            st.warning("Kolom 'Condition' tidak ditemukan dalam dataset.")

        fig.update_layout(
            title=f'Diagram Pie Keamanan untuk {selected_country} pada Tahun {selected_year if selected_year != "Semua Tahun" else "Semua Tahun"}',
            margin=dict(l=0, r=0, b=0, t=80),
            colorway=['#54B435', '#39A7FF', '#D80032'],  # Mengatur margin agar diagram tidak terpotong
        )
        st.plotly_chart(fig)
    else:
        st.warning("Data tidak tersedia untuk ditampilkan.")

# Jika memilih "Alert System"
else:
    # Subjudul untuk bagian alert system
    st.text("Alert System")

    # Menampilkan pilihan selectbox untuk alert system
    selected_year_alert = st.selectbox("Pilih Tahun:", ['2023'])
          # Urutkan negara secara alfabetis
    countries_sorted_alert = sorted(datSet['Country'].unique())
    selected_country_alert = st.selectbox("Pilih Negara:", ['Semua Negara'] + countries_sorted_alert)

    # Menambahkan alert
    if selected_country_alert != 'Semua Negara':
        # Filter data berdasarkan negara
        country_data_alert = datSet[datSet['Country'] == selected_country_alert]

        # Filter data untuk 3 tahun terakhir
        last_three_years_data_alert = country_data_alert[country_data_alert['year'].isin(country_data_alert['year'].unique()[-3:])]

        # Cek apakah terjadi penurunan indeks OVERALL SCORE
        if last_three_years_data_alert['Overall Scores'].diff().sum() < 0:
            st.success("Negara ini mengalami penurunan indeks OVERALL SCORE dalam 3 tahun terakhir.")
        else:
            st.warning("Negara ini tidak mengalami penurunan indeks OVERALL SCORE dalam 3 tahun terakhir. Berpotensi naik pada tahun berikutnya.")
