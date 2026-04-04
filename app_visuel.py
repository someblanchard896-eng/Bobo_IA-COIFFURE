import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✂️", layout="wide")

# --- CONNEXION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def charger_donnees():
    try:
        data = conn.read(spreadsheet="Base_Blanco_Beaute", worksheet="Salons", ttl=0)
        return data
    except:
        return pd.DataFrame(columns=['nom', 'type', 'ville', 'secteur', 'tel', 'photo_url', 'video_url', 'revenus'])

def enregistrer_donnees(df):
    conn.update(spreadsheet="Base_Blanco_Beaute", worksheet="Salons", data=df)

df_actuel = charger_donnees()

# --- DONNÉES ---
villes_dispo = ["Bobo-Dioulasso", "Ouagadougou"]
secteurs_dict = {
    "Bobo-Dioulasso": [
        "Secteur 1 (Dioulassoba)", "Secteur 2 (Dogona)", "Secteur 2 (Accart-ville)", 
        "Secteur 3 (Tounouma)", "Secteur 4 (Koko)", "Secteur 10 (Accart-ville Nord)", 
        "Secteur 10 (Yéguéré)", "Secteur 17 (Sarfalao)", "Secteur 21 (Colma)", 
        "Secteur 22 (Belle-Ville)", "Secteur 25"
    ],
    "Ouagadougou": [
        "Ouaga 2000", "Pissy", "Tampouy", "Dassasgho", "Patte d'Oie", 
        "Gounghin", "Karpala", "Secteur 15", "Secteur 30"
    ]
}

menu = st.sidebar.radio("Navigation", ["🏠 Accueil Clients", "🔐 Espace Admin"])

# ================= PAGE ACCUEIL =================
if menu == "🏠 Accueil Clients":
    st.title("✨ Blanco Beauté Connect")
    
    v_choisie = st.selectbox("📍 Choisissez votre ville", ["-- Sélectionner --"] + villes_dispo)
    
    if v_choisie != "-- Sélectionner --":
        q_choisi = st.selectbox(f"🏘️ Quartier à {v_choisie}", ["-- Tous les quartiers --"] + secteurs_dict[v_choisie])
        
        df_filtre = df_actuel[df_actuel['ville'] == v_choisie]
        if q_choisi != "-- Tous les quartiers --":
            df_filtre = df_filtre[df_filtre['secteur'] == q_choisi]
            
        st.divider()
        
        if df_filtre.empty:
            st.info("Aucun salon disponible ici pour le moment.")
        else:
            for _, row in df_filtre.iterrows():
                with st.expander(f"✨ {row['nom']} ({row['secteur']})"):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        img = row['photo_url'] if pd.notnull(row['photo_url']) and row['photo_url'] != "" else "https://via.placeholder.com/400x300?text=Blanco+Beauté"
                        st.image(img, use_container_width=True)
                        if pd.notnull(row['video_url']) and row['video_url'] != "":
                            st.video(row['video_url'])
                    
                    with col2:
                        st.subheader(row['nom'])
                        st.write(f"🏠 **Quartier :** {row['secteur']}")
                        st.write(f"🏷️ **Catégorie :** {row['type']}")
                        
                        st.write("---")
                        st.write("### 📅 RÉSERVER MAINTENANT")
                        
                        # Nettoyage du numéro
                        num = str(row['tel']).replace(" ", "")
                        if not num.startswith('226'): num = '226' + num
                        
                        # --- BOUTONS DE RÉSERVATION ---
                        c_simple, c_mariage = st.columns(2)
                        
                        with c_simple:
                            msg_s = urllib.parse.quote(f"Bonjour {row['nom']}, je souhaite faire une RÉSERVATION SIMPLE chez vous via Blanco Connect.")
                            st.link_button("💇 Coiffure Simple", f"https://wa.me/{num}?text={msg_s}")
                            
                        with c_mariage:
                            msg_m = urllib.parse.quote(f"Bonjour {row['nom']}, je souhaite faire une RÉSERVATION MARIAGE chez vous via Blanco Connect.")
                            st.link_button("👰 Spécial Mariage", f"https://wa.me/{num}?text={msg_m}")

# ================= PAGE ADMIN =================
elif menu == "🔐 Espace Admin":
    if st.sidebar.text_input("Code secret", type="password") == "Blanco.10":
        st.header("⚙️ Administration")
        with st.form("nouveau_salon"):
            nom = st.text_input("Nom du Salon")
            col_v, col_s = st.columns(2)
            with col_v: v = st.selectbox("Ville", villes_dispo)
            with col_s: s = st.selectbox("Quartier", secteurs_dict[v])
            
            # Ici on garde le type général du salon
            t = st.selectbox("Spécialité principale", ["Coiffure Homme", "Coiffure Femme", "Institut complet", "Mixte"])
            tel = st.text_input("WhatsApp (ex: 70000000)")
            p_url = st.text_input("Lien Photo (URL)")
            v_url = st.text_input("Lien Vidéo (YouTube/TikTok)")
            
            if st.form_submit_button("🚀 Publier le Salon"):
                if nom and tel:
                    nouveau = pd.DataFrame([{"nom": nom, "type": t, "ville": v, "secteur": s, "tel": tel, "photo_url": p_url, "video_url": v_url, "revenus": 0}])
                    df_final = pd.concat([df_actuel, nouveau], ignore_index=True)
                    enregistrer_donnees(df_final)
                    st.success(f"Salon {nom} ajouté !")
                    st.rerun()
