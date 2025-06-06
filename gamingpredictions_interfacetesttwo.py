# -*- coding: utf-8 -*-
"""gamingpredictions_interfacetesttwo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I4mbYgJz0cFaETLXScmT2Oxlr_JATMH3
"""



import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

# Configurações iniciais de layout
st.set_page_config(layout="centered", page_title="Previsão de Vendas", page_icon="📈")

# Dataset (ajuste o caminho conforme sua hospedagem)
@st.cache_data
def load_data():
    df = pd.read_csv("gaming_industry_trends.csv")
    return df

df = load_data()

# Funções de previsão por plataforma
def previsao_por_plataforma(df):
    grouped_df = df.groupby(['Platform', 'Release Year'])
    new_data = []

    for (platform, year), group in grouped_df:
        group_data = {'Platform': platform, 'Release Year': year}
        text_columns = ['Developer', 'Genre', 'Esports Popularity', 'Trending Status']
        for col in text_columns:
            group[col] = group[col].astype(str)
        group['combined_text'] = group[text_columns].apply(lambda row: ' '.join(row), axis=1)
        vectorizer = CountVectorizer()
        vectorized_data = vectorizer.fit_transform(group['combined_text'])
        feature_names = vectorizer.get_feature_names_out()
        for i, feature in enumerate(feature_names):
            group_data[feature] = vectorized_data.toarray()[0][i]
        for col in ['Players (Millions)', 'Peak Concurrent Players', 'Metacritic Score']:
            group_data[f'{col}_mean'] = group[col].mean()
        group_data['Revenue (Millions $)_sum'] = group['Revenue (Millions $)'].sum()
        new_data.append(group_data)

    new_df = pd.DataFrame(new_data).fillna(-1000)
    new_df = new_df.rename(columns={'Revenue (Millions $)_sum': 'revenue_sum'})
    features = [col for col in new_df.columns if col not in ['Platform', 'Release Year', 'revenue_sum']]
    X = new_df[features]
    y = new_df['revenue_sum']
    X_train = X[new_df['Release Year'] < 2020]
    y_train = y[new_df['Release Year'] < 2020]
    X_test = X[new_df['Release Year'] >= 2020]
    y_test = y[new_df['Release Year'] >= 2020]

    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X)

    platforms = new_df['Platform'].unique()
    for platform in platforms:
        platform_data = new_df[new_df['Platform'] == platform]
        years = platform_data['Release Year']
        real = platform_data['revenue_sum']
        pred = y_pred[new_df['Platform'] == platform]

        fig, ax = plt.subplots()
        ax.plot(years, real, label='Real', marker='o')
        ax.plot(years[years >= 2020], pred[years >= 2020], label='Previsto', marker='x')
        ax.set_title(f'Previsão de Receita: {platform}')
        ax.set_xlabel("Ano")
        ax.set_ylabel("Receita (milhões $)")
        ax.legend()
        st.pyplot(fig)

# Função de previsão por gênero
def previsao_por_genero(df):
    grouped_df = df.groupby(['Genre', 'Release Year'])
    new_data = []

    for (genre, year), group in grouped_df:
        group_data = {'Genre': genre, 'Release Year': year}
        text_columns = ['Developer', 'Platform', 'Esports Popularity', 'Trending Status']
        for col in text_columns:
            group[col] = group[col].astype(str)
        group['combined_text'] = group[text_columns].apply(lambda row: ' '.join(row), axis=1)
        vectorizer = CountVectorizer()
        vectorized_data = vectorizer.fit_transform(group['combined_text'])
        feature_names = vectorizer.get_feature_names_out()
        for i, feature in enumerate(feature_names):
            group_data[feature] = vectorized_data.toarray()[0][i]
        for col in ['Players (Millions)', 'Peak Concurrent Players', 'Metacritic Score']:
            group_data[f'{col}_mean'] = group[col].mean()
        group_data['Revenue (Millions $)_sum'] = group['Revenue (Millions $)'].sum()
        new_data.append(group_data)

    new_df = pd.DataFrame(new_data).fillna(-1000)
    new_df = new_df.rename(columns={'Revenue (Millions $)_sum': 'revenue_sum'})
    features = [col for col in new_df.columns if col not in ['Genre', 'Release Year', 'revenue_sum']]
    X = new_df[features]
    y = new_df['revenue_sum']
    X_train = X[new_df['Release Year'] < 2020]
    y_train = y[new_df['Release Year'] < 2020]
    X_test = X[new_df['Release Year'] >= 2020]
    y_test = y[new_df['Release Year'] >= 2020]

    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X)

    genres = new_df['Genre'].unique()
    for genre in genres:
        genre_data = new_df[new_df['Genre'] == genre]
        years = genre_data['Release Year']
        real = genre_data['revenue_sum']
        pred = y_pred[new_df['Genre'] == genre]

        fig, ax = plt.subplots()
        ax.plot(years, real, label='Real', marker='o')
        ax.plot(years[years >= 2020], pred[years >= 2020], label='Previsto', marker='x')
        ax.set_title(f'Previsão de Receita: {genre}')
        ax.set_xlabel("Ano")
        ax.set_ylabel("Receita (milhões $)")
        ax.legend()
        st.pyplot(fig)

import streamlit as st
from PIL import Image

# Carrega imagens
icon = Image.open("icon-removebg-preview.png")
img_plataforma = Image.open("plataforma-removebg-preview.png")
img_genero = Image.open("genero-removebg-preview.png")

# Aplica CSS para o fundo
st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom, #546A7B, #000000);
    }
    .stApp {
        background: linear-gradient(to bottom, #546A7B, #000000);
    }
    .title {
        text-align: center;
        font-size: 32px;
        color: white;
        margin-top: -20px;
    }
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar com estado de navegação
if 'tela' not in st.session_state:
    st.session_state.tela = 'inicio'

# Navegação entre telas
if st.session_state.tela == 'inicio':
    st.image(icon, width=120)
    st.markdown("<h1 class='title'>Previsão de Vendas</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Previsão por Plataforma"):
            st.session_state.tela = 'plataforma'
    with col2:
        if st.button("Previsão por Gênero"):
            st.session_state.tela = 'genero'

    with col1:
        st.image(img_plataforma, width=80)
    with col2:
        st.image(img_genero, width=80)

elif st.session_state.tela == 'plataforma':
    st.button("⬅ Voltar", on_click=lambda: st.session_state.update({'tela': 'inicio'}))
    previsao_por_plataforma()

elif st.session_state.tela == 'genero':
    st.button("⬅ Voltar", on_click=lambda: st.session_state.update({'tela': 'inicio'}))
    previsao_por_genero()