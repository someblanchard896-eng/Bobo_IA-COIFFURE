import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd
import time

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté | L'Éclat du Faso", page_icon="✨", layout="centered")

# --- CONNEXION GOOGLE SHEETS ---
@st.cache_resource
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Base_Blanco_Beaute").sheet1
    except Exception as e: return str(e)

sheet = connect_to_sheet()

def load_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df_salons = load_data()

# --- DESIGN CSS (Version Luxe) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .salon-card { border: 1px solid #eee; padding: 20px; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid #d4af37; }
    .gold-text { color: #d4af37; font-weight: bold; }
    .stButton>button { background-color: #000; color: #d4af37; border: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- ADMINISTRATION ---
with st.sidebar:
    st.title("🔱 Admin Empire")
    pwd = st.text_input("Code Secret", type="password")
    if pwd == "Blanco.10":
        st.success("Accès Autorisé")
        if st.button("🗑️ Nettoyer le Cache"):
            st.cache_resource.clear()
            st.rerun()

# --- ACCUEIL ---
st.markdown("<h1 style='text-align:center; color:#d4af37;'>FASO BEAUTÉ</h1>", unsafe_allow_html=True)

v_c = st.selectbox("📍 Ville", ["OUAGADOUGOU", "BOBO-DIOULASSO"])
q_c = st.text_input("🏘️ Quartier (ex: Ouaga 2000, Secteur 22)")

results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'].str.contains(q_c, case=False))]

if not results.empty:
    for idx, row in results.iterrows():
        # Ligne réelle dans Google Sheets (index + 2 car index 0 = ligne 2)
        sheet_row = idx + 2 
        
        st.markdown(f'<div class="salon-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.image(row['lien photo'] if row['lien photo'] else "https://via.placeholder.com/150")
            # --- PORTFOLIO DYNAMIQUE ---
            p_col1, p_col2 = st.columns(2)
            if row.get('photo_2'): p_col1.image(row['photo_2'])
            if row.get('photo_3'): p_col2.image(row['photo_3'])
        
        with col2:
            st.subheader(row['nom du salon'])
            # --- SYSTÈME DE NOTES ---
            note = row.get('avis_moyenne', 5)
            st.markdown(f"<span class='gold-text'>{'⭐' * int(note)} ({row.get('nb_avis', 0)} avis)</span>", unsafe_allow_html=True)
            
            # --- FONCTIONNALITÉ : NOTER (Calcul automatique) ---
            with st.expander("⭐ Noter ce salon"):
                new_grade = st.select_slider("Ma note", options=[1, 2, 3, 4, 5], key=f"grade_{idx}")
                if st.button("Valider la note", key=f"btn_grade_{idx}"):
                    old_nb = int(row.get('nb_avis', 0))
                    old_avg = float(row.get('avis_moyenne', 5))
                    # Algorithme de moyenne mobile
                    new_nb = old_nb + 1
                    new_avg = ((old_avg * old_nb) + new_grade) / new_nb
                    
                    # Mise à jour Google Sheets (Colonnes K et L)
                    sheet.update_cell(sheet_row, 11, round(new_avg, 1))
                    sheet.update_cell(sheet_row, 12, new_nb)
                    st.success("Note enregistrée !")
                    st.rerun()

            # --- RÉSERVATION ---
            if st.button(f"RÉSERVER", key=f"res_{idx}"):
                # Mise à jour Revenus (Colonne G)
                nouveau_revenu = int(row.get('revenus', 0)) + 500 # Simule un acompte
                sheet.update_cell(sheet_row, 7, nouveau_revenu)
                
                msg = urllib.parse.quote(f"Bonjour, je souhaite réserver au salon {row['nom du salon']} via Faso Beauté.")
                st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px;">📲 CONFIRMER WHATSAPP</button></a>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
