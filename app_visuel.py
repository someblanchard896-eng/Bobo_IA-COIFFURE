import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✨", layout="wide")

# --- CONNEXION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def charger_donnees():
    try:
        # Lecture sécurisée
        data = conn.read(spreadsheet="Base_Blanco_Beaute", worksheet="Salons", ttl=0)
        return data
    except:
        # Structure de secours si Google est capricieux
        return pd.DataFrame(columns=['nom', 'type', 'ville', 'secteur', 'tel', 'photo_url', 'revenus'])

def enregistrer_donnees(df):
    # On force la mise à jour vers Google
    conn.update(spreadsheet="Base_Blanco_Beaute", worksheet="Salons", data=df)

# --- CHARGEMENT ---
df_actuel = charger_donnees()

# --- MENU LATÉRAL ---
menu = st.sidebar.radio("Navigation", ["🏠 Accueil", "🔐 Gestion Blanco"])

# ================= PAGE ACCUEIL (PUBLIC) =================
if menu == "🏠 Accueil":
    st.title("✨ Bienvenue chez Blanco Beauté")
    st.subheader("Trouvez votre salon de coiffure au Burkina")
    
    if df_actuel.empty:
        st.info("Aucun salon n'est encore enregistré.")
    else:
        # Affichage des salons sous forme de cartes simples
        for index, row in df_actuel.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col2:
                    st.markdown(f"### {row['nom']}")
                    st.write(f"📍 {row['ville']} - {row['secteur']}")
                    st.write(f"📞 WhatsApp : {row['tel']}")
                st.divider()

# ================= PAGE ADMIN (MOT DE PASSE) =================
elif menu == "🔐 Gestion Blanco":
    pwd = st.sidebar.text_input("Code secret :", type="password")
    if pwd == "Blanco.10":
        st.header("👨‍💼 Administration")
        
        with st.expander("➕ Ajouter un nouveau Salon"):
            with st.form("ajout_salon"):
                n = st.text_input("Nom du Salon")
                t = st.selectbox("Type", ["Coiffure Homme", "Coiffure Femme", "Institut Beauté"])
                v = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
                s = st.text_input("Secteur (ex: Secteur 21)")
                tel = st.text_input("WhatsApp (ex: 70600000)")
                
                if st.form_submit_button("Enregistrer le Salon"):
                    if n and tel:
                        # Création de la ligne avec les 7 colonnes
                        nouveau = pd.DataFrame([{
                            "nom": n, "type": t, "ville": v, "secteur": s, 
                            "tel": tel, "photo_url": "", "revenus": 0
                        }])
                        df_final = pd.concat([df_actuel, nouveau], ignore_index=True)
                        
                        try:
                            enregistrer_donnees(df_final)
                            st.success("✅ Salon ajouté au Cloud !")
                            st.balloons()
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Google bloque encore : {e}")
                            st.info("Vérifie que l'e-mail du robot est bien 'Éditeur' sur ton Google Sheets.")
    else:
        st.warning("Veuillez entrer le code secret pour accéder à la gestion.")
