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
        # S'assurer que les colonnes sont propres
        data.columns = [c.lower() for c in data.columns]
        return data
    except:
        return pd.DataFrame(columns=['nom', 'type', 'ville', 'secteur', 'tel', 'photo_url', 'revenus'])

def enregistrer_donnees(df):
    conn.update(spreadsheet="Base_Blanco_Beaute", worksheet="Salons", data=df)

df_actuel = charger_donnees()

# --- LISTES DES SECTEURS ---
secteurs_bobo = ["Secteur 1", "Secteur 2 (Dogona)", "Secteur 3 (Tounouma)", "Secteur 4", "Secteur 10 (Yéguéré)", "Secteur 17 (Sarfalao)", "Secteur 21 (Colma)", "Secteur 22", "Secteur 25"]
secteurs_ouaga = ["Ouaga 2000", "Pissy", "Tampouy", "Dassasgho", "Patte d'Oie", "Gounghin", "Karpala", "Secteur 15", "Secteur 30"]
tous_secteurs = sorted(list(set(secteurs_bobo + secteurs_ouaga)))

# --- MENU ---
menu = st.sidebar.radio("Navigation", ["🏠 Accueil Clients", "🔐 Gestion Blanco"])

# ================= PAGE ACCUEIL (RECHERCHE AUTO) =================
if menu == "🏠 Accueil Clients":
    st.title("✨ Blanco Beauté Connect")
    st.markdown("#### Trouvez votre style dans les meilleurs salons du Burkina")
    
    # Barre de recherche intelligente
    recherche = st.multiselect("📍 Tapez ou choisissez votre secteur/quartier :", options=tous_secteurs, placeholder="Ex: Secteur 21...")

    st.divider()

    # Filtrage
    df_affiche = df_actuel.copy()
    if recherche:
        df_affiche = df_affiche[df_affiche['secteur'].isin(recherche)]

    if df_affiche.empty:
        st.info("Utilisez la barre de recherche ci-dessus pour trouver un salon par secteur.")
    else:
        for _, row in df_affiche.iterrows():
            with st.container():
                col_img, col_txt = st.columns([1, 2])
                
                with col_img:
                    # Gestion de l'image
                    url_img = row['photo_url'] if pd.notnull(row['photo_url']) and row['photo_url'] != "" else "https://img.freepik.com/vecteurs-libre/logo-salon-coiffure-vintage-isole-blanc_44392-111.jpg"
                    st.image(url_img, use_container_width=True)
                
                with col_txt:
                    st.subheader(f"{row['nom']}")
                    st.caption(f"⭐ {row['type']} | 📍 {row['ville']}")
                    st.write(f"🏠 **Secteur :** {row['secteur']}")
                    
                    # WhatsApp
                    num = str(row['tel']).replace(" ", "")
                    if not num.startswith('226'): num = '226' + num
                    msg = urllib.parse.quote(f"Bonjour {row['nom']}, je vous contacte via l'app Blanco Beauté !")
                    st.link_button("🟢 Contacter sur WhatsApp", f"https://wa.me/{num}?text={msg}")
                st.divider()

# ================= PAGE ADMIN (AJOUT AVEC PHOTO) =================
elif menu == "🔐 Gestion Blanco":
    if st.sidebar.text_input("Code secret", type="password") == "Blanco.10":
        st.header("⚙️ Administration")
        
        with st.form("ajout"):
            n = st.text_input("Nom du Salon")
            col1, col2 = st.columns(2)
            with col1:
                v = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
                t = st.selectbox("Prestation", ["Coiffure Homme", "Coiffure Femme", "Mariage", "Institut Beauté"])
            with col2:
                s = st.selectbox("Secteur", secteurs_bobo if v == "Bobo-Dioulasso" else secteurs_ouaga)
                tel = st.text_input("WhatsApp (ex: 70000000)")
            
            p_url = st.text_input("Lien de la photo (URL)", placeholder="Collez ici le lien d'une image Facebook ou Google")
            
            if st.form_submit_button("🚀 Publier le Salon"):
                if n and tel:
                    nouveau = pd.DataFrame([{"nom": n, "type": t, "ville": v, "secteur": s, "tel": tel, "photo_url": p_url, "revenus": 0}])
                    df_final = pd.concat([df_actuel, nouveau], ignore_index=True)
                    enregistrer_donnees(df_final)
                    st.success("Salon ajouté avec succès !")
                    st.rerun()
