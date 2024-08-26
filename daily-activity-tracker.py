import streamlit as st
import sqlite3
from datetime import datetime

# Initialize the database
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

# Save entry to the database
def save_entry(date, content, emotion):
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO diary (date, content, emotion) VALUES (?, ?, ?)
    ''', (date, content, emotion))
    conn.commit()
    conn.close()

# Retrieve entries from the database
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

# Define the main application
def main():
    st.title("Daily Activity Tracker App")
    st.write("Enter your diary entry and rate your mood.")

    # User input
    date = st.date_input("Select a date", datetime.now())
    content = st.text_area("Enter your diary entry here")
    emotion = st.slider("Rate your mood from 1 to 10 (1: feeling down, 10: very happy)", 1, 10, 5)

    if st.button("Save"):
        if content:
            save_entry(date.strftime('%Y-%m-%d'), content, emotion)
            st.success("Your diary entry has been saved.")
        else:
            st.error("Please enter the content of your diary.")

    # Display saved diary entries
    st.write("## Saved Diary Entries")
    entries = get_entries()
    for entry in entries:
        st.write(f"**Date:** {entry[0]}")
        st.write(f"**Content:** {entry[1]}")
        st.write(f"**Emotion Score:** {entry[2]}")
        st.write("---")

if __name__ == "__main__":
    init_db()
    main()
