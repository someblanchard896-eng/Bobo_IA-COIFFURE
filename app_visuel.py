import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✨", layout="wide")

# URL de ton Google Sheets (celui que tu m'as envoyé)
url_gsheet = "https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJlY3s/edit?usp=sharing"

# --- CONNEXION À LA BASE DE DONNÉES ---
conn = st.connection("gsheets", type=GSheetsConnection)

def charger_donnees():
    return conn.read(spreadsheet=url_gsheet, usecols=[0,1,2,3,4,5,6], ttl=0)

def enregistrer_donnees(df):
    conn.update(spreadsheet=url_gsheet, data=df)

# --- LISTES DES SECTEURS ---
options_bobo = [
    "Secteur 1 (Dioulassoba)", "Secteur 2 (Dogona)", "Secteur 2 (Accart-ville)", 
    "Secteur 3 (Tounouma)", "Secteur 4 (Koko)", "Secteur 5 (Kyé)", "Secteur 6 (Koua)", 
    "Secteur 7 (Bolomakoté)", "Secteur 8 (Sikasso-Cira)", "Secteur 9 (Sya/Kuin-Nima)", 
    "Secteur 10 (Accart-ville Nord)", "Secteur 10 (Yéguéré)", "Secteur 11 (Colma)", 
    "Secteur 12 (Bolomakoté)", "Secteur 13 (Saint-Étienne)", "Secteur 14 (Bindougousso)", 
    "Secteur 15 (Ouezzin-Ville)", "Secteur 17 (Sarfalao)", "Secteur 21 (Colma)", 
    "Secteur 22 (Belle-Ville)", "Secteur 24", "Secteur 25", "Secteur 31"
]

options_ouaga = ["Ouaga 2000", "Pissy", "Tampouy", "Dassasgho", "Patte d'Oie", "Gounghin", "Karpala", "Secteur 30", "Larlé"]

# --- NAVIGATION ---
menu = st.sidebar.radio("MENU", ["🏠 ACCUEIL CLIENTS", "🔐 GESTION BLANCO"])

df_actuel = charger_donnees()

# ================= PARTIE CLIENTS =================
if menu == "🏠 ACCUEIL CLIENTS":
    st.header("✨ Salons de Coiffure & Beauté")
    
    col_v, col_q = st.columns(2)
    with col_v:
        v_nom = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
    with col_q:
        liste = sorted(options_bobo) if v_nom == "Bobo-Dioulasso" else sorted(options_ouaga)
        s_nom = st.selectbox("Quartier", options=liste, index=None, placeholder="Cherchez votre quartier...")

    if s_nom:
        filtre = df_actuel[(df_actuel['ville'] == v_nom) & (df_actuel['secteur'] == s_nom)]
        
        if filtre.empty:
            st.info(f"📍 Aucun établissement disponible au **{s_nom}**.")
        else:
            for i, row in filtre.iterrows():
                with st.container():
                    st.markdown(f"### {row['nom']} — *{row['type']}*")
                    
                    # Choix Prestation
                    type_res = st.radio(f"Prestation chez {row['nom']} :", ["Simple", "Mariage"], key=f"res_{i}", horizontal=True)
                    
                    # Lien WhatsApp
                    msg = f"Bonjour, je réserve une séance *{type_res}* via Blanco Beauté."
                    link = f"https://wa.me/226{row['tel']}?text={msg.replace(' ', '%20')}"
                    
                    st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366; color:white; text-align:center; padding:12px; border-radius:10px; font-weight:bold;">💬 RÉSERVER ({type_res.upper()})</div></a>', unsafe_allow_html=True)
                    
                    # LE BOUTON QUI PAYE (AJOUTE 100F AU GSHEET)
                    if st.button(f"Confirmer ma visite chez {row['nom']}", key=f"btn_{i}"):
                        df_actuel.at[i, 'revenu'] = int(df_actuel.at[i, 'revenu']) + 100
                        enregistrer_donnees(df_actuel)
                        st.success("✅ Gain de 100 F enregistré !")
                        st.balloons()
                    st.divider()

# ================= PARTIE ADMIN =================
elif menu == "🔐 GESTION BLANCO":
    pwd = st.sidebar.text_input("Code secret :", type="password")
    if pwd == "Blanco.10":
        st.header("🛠️ Administration Blanco")
        
        with st.form("ajout_salon"):
            n = st.text_input("Nom du Salon")
            t = st.selectbox("Type", ["Coiffure", "Beauté", "Mixte"])
            v = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
            s = st.selectbox("Secteur", options=sorted(options_bobo) if v == "Bobo-Dioulasso" else sorted(options_ouaga))
            tel = st.text_input("WhatsApp (ex: 70000000)")
            
            if st.form_submit_button("Enregistrer"):
                nouveau = pd.DataFrame([{"nom":n, "type":t, "ville":v, "secteur":s, "tel":tel, "photo_url":"", "revenu":0}])
                df_final = pd.concat([df_actuel, nouveau], ignore_index=True)
                enregistrer_donnees(df_final)
                st.success("Salon ajouté dans Google Sheets !")

        st.subheader("💰 Tes Gains Réels")
        st.dataframe(df_actuel[['nom', 'secteur', 'revenu']])
