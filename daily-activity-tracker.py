import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import altair as alt

# データベース接続
conn = sqlite3.connect('activity_data.db')
c = conn.cursor()

# テーブルの作成（存在しない場合）
c.execute('''
    CREATE TABLE IF NOT EXISTS activities
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     date TEXT,
     category TEXT,
     activity TEXT,
     mood_score INTEGER)
''')
conn.commit()

# アプリのタイトル
st.title('日々の活動記録アプリ')

# データの読み込み
@st.cache_data
def load_data():
    return pd.read_sql_query("SELECT * from activities", conn)

# 入力フォーム
with st.form("activity_form"):
    date = st.date_input('日付', datetime.now())
    category = st.selectbox('カテゴリ', ['仕事', '運動', '趣味', '学習', 'その他'])
    activity = st.text_area('活動の詳細', height=100)
    mood = st.slider('気分スコア', 1, 10, 5)
    
    submitted = st.form_submit_button('記録を追加')
    if submitted:
        c.execute('''
            INSERT INTO activities (date, category, activity, mood_score)
            VALUES (?, ?, ?, ?)
        ''', (date.strftime('%Y-%m-%d'), category, activity, mood))
        conn.commit()
        st.success('記録が追加されました！')
        st.experimental_rerun()

# データの表示
df = load_data()

tab1, tab2, tab3 = st.tabs(["記録一覧", "統計情報", "グラフ"])

with tab1:
    st.subheader('これまでの記録')
    st.dataframe(df.sort_values('date', ascending=False), use_container_width=True)

with tab2:
    st.subheader('統計情報')
    col1, col2 = st.columns(2)
    with col1:
        st.metric("合計記録数", len(df))
    with col2:
        st.metric("平均気分スコア", f"{df['mood_score'].mean():.2f}")

with tab3:
    st.subheader('カテゴリ別記録数')
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['カテゴリ', '記録数']
    
    chart = alt.Chart(category_counts).mark_bar().encode(
        x='カテゴリ',
        y='記録数',
        color='カテゴリ'
    ).properties(
        width=alt.Step(80)
    )
    st.altair_chart(chart, use_container_width=True)

    st.subheader('気分スコアの推移')
    df_sorted = df.sort_values('date')
    line_chart = alt.Chart(df_sorted).mark_line().encode(
        x='date:T',
        y='mood_score:Q',
        tooltip=['date', 'mood_score', 'category', 'activity']
    ).properties(
        width=600,
        height=300
    )
    st.altair_chart(line_chart, use_container_width=True)

# データベース接続を閉じる
conn.close()