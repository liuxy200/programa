
import streamlit as st
import instaloader
import csv
import os

def get_following(username, session_user, session_pass):
    L = instaloader.Instaloader()
    L.login(session_user, session_pass)
    profile = instaloader.Profile.from_username(L.context, username)
    
    filename = f"{username}_following.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Full Name"])
        for followee in profile.get_followees():
            writer.writerow([followee.username, followee.full_name])
    
    return filename

st.title("Instagram Following List Downloader")

session_user = st.text_input("Tu usuario de Instagram")
session_pass = st.text_input("Tu contraseña de Instagram", type="password")
username = st.text_input("Usuario del que quieres obtener la lista de seguidos")

if st.button("Obtener lista de seguidos"):
    if session_user and session_pass and username:
        with st.spinner("Obteniendo lista de seguidos..."):
            try:
                file_path = get_following(username, session_user, session_pass)
                st.success("¡Lista obtenida con éxito!")
                st.download_button(label="Descargar CSV", data=open(file_path, "rb").read(), file_name=file_path, mime="text/csv")
                os.remove(file_path)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Por favor, ingresa todos los datos.")
