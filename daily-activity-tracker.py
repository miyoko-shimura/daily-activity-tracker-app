import streamlit as st
import sqlite3
from datetime import datetime

# データベースの初期化
def init_db():
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY,
            date TEXT,
            content TEXT,
            emotion INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# データの保存
def save_entry(content, emotion):
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO diary (date, content, emotion) VALUES (?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), content, emotion))
    conn.commit()
    conn.close()

# データの読み込み
def get_entries():
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute('''
        SELECT date, content, emotion FROM diary
        ORDER BY date DESC
    ''')
    entries = c.fetchall()
    conn.close()
    return entries

# メインアプリの定義
def main():
    st.title("日記アプリ")
    st.write("日記を入力し、感情を1から10で評価してください。")

    # ユーザーの入力
    content = st.text_area("日記を入力してください")
    emotion = st.slider("感情を1から10で評価してください", 1, 10, 5)

    if st.button("保存"):
        if content:
            save_entry(content, emotion)
            st.success("日記が保存されました。")
        else:
            st.error("日記の内容を入力してください。")

    # 保存された日記の表示
    st.write("## 保存された日記")
    entries = get_entries()
    for entry in entries:
        st.write(f"**日時:** {entry[0]}")
        st.write(f"**内容:** {entry[1]}")
        st.write(f"**感情スコア:** {entry[2]}")
        st.write("---")

if __name__ == "__main__":
    init_db()
    main()
