import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✨", layout="wide")

# TON NOUVEAU LIEN (Vérifié)
url_gsheet = "https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJlY3s/edit?usp=sharing"

# --- CONNEXION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def charger_donnees():
    try:
        # On lit les 7 colonnes (A à G)
        data = conn.read(spreadsheet=url_gsheet, ttl=0)
        return data
    except:
        # Si le tableau est illisible, on crée une structure vide
        return pd.DataFrame(columns=['nom', 'type', 'ville', 'secteur', 'tel', 'photo_url', 'revenu'])

def enregistrer_donnees(df):
    conn.update(spreadsheet=url_gsheet, data=df)

# --- LISTES DES SECTEURS ---
options_bobo = [
    "Secteur 1 (Dioulassoba)", "Secteur 2 (Dogona)", "Secteur 2 (Accart-ville)", 
    "Secteur 3 (Tounouma)", "Secteur 4 (Koko)", "Secteur 10 (Accart-ville Nord)", 
    "Secteur 10 (Yéguéré)", "Secteur 17 (Sarfalao)", "Secteur 21 (Colma)", "Secteur 22 (Belle-Ville)"
]
options_ouaga = ["Ouaga 2000", "Pissy", "Tampouy", "Dassasgho", "Patte d'Oie", "Gounghin", "Karpala"]

# --- CHARGEMENT ---
df_actuel = charger_donnees()

# --- NAVIGATION ---
menu = st.sidebar.radio("MENU", ["🏠 ACCUEIL CLIENTS", "🔐 GESTION BLANCO"])

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
        if not df_actuel.empty and 'ville' in df_actuel.columns:
            filtre = df_actuel[(df_actuel['ville'] == v_nom) & (df_actuel['secteur'] == s_nom)]
            
            if filtre.empty:
                st.info(f"📍 Aucun établissement disponible au *{s_nom}*.")
            else:
                for i, row in filtre.iterrows():
                    with st.container():
                        st.subheader(f"{row['nom']} ({row['type']})")
                        
                        type_res = st.radio(f"Prestation :", ["Simple", "Mariage"], key=f"res_{i}", horizontal=True)
                        
                        # Lien WhatsApp
                        link = f"https://wa.me/226{row['tel']}?text=Bonjour%2C%20je%20réserve%20une%20séance%20{type_res}%20via%20Blanco%20Beauté."
                        
                        st.markdown(f'''
                            <a href="{link}" target="_blank" style="text-decoration:none;">
                                <div style="background-color:#25D366; color:white; text-align:center; padding:12px; border-radius:10px; font-weight:bold;">
                                    💬 RÉSERVER ({type_res.upper()})
                                </div>
                            </a>
                        ''', unsafe_allow_html=True)
                        
                        if st.button(f"Confirmer réservation chez {row['nom']}", key=f"pay_{i}"):
                            # Mise à jour du revenu (100f)
                            df_actuel.at[i, 'revenu'] = int(df_actuel.at[i, 'revenu']) + 100
                            enregistrer_donnees(df_actuel)
                            st.success("Gain de 100 F enregistré dans le Google Sheets !")
                            st.balloons()
                        st.divider()
        else:
            st.info("Ajoutez d'abord des salons dans la partie Gestion.")

# ================= PARTIE ADMIN =================
elif menu == "🔐 GESTION BLANCO":
    pwd = st.sidebar.text_input("Code secret :", type="password")
    if pwd == "Blanco.10":
        st.header("🛠️ Administration Blanco")
        
        with st.expander("Ajouter un nouveau Salon"):
            with st.form("ajout_salon"):
                n = st.text_input("Nom du Salon")
                t = st.selectbox("Type", ["Coiffure Homme", "Coiffure Femme", "Institut Beauté", "Mariage"])
                v = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
                s = st.selectbox("Secteur", options=sorted(options_bobo) if v == "Bobo-Dioulasso" else sorted(options_ouaga))
                tel = st.text_input("WhatsApp (ex: 70000000)")
                
                if st.form_submit_button("Enregistrer"):
                    nouveau = pd.DataFrame([{"nom":n, "type":t, "ville":v, "secteur":s, "tel":tel, "photo_url":"", "revenu":0}])
                    df_final = pd.concat([df_actuel, nouveau], ignore_index=True)
                    enregistrer_donnees(df_final)
                    st.success(f"Le salon {n} a été ajouté au Google Sheets !")
                    st.rerun()

        if not df_actuel.empty:
            st.subheader("💰 Suivi de tes gains")
            total = pd.to_numeric(df_actuel['revenu']).sum()
            st.metric("TOTAL COLLECTÉ", f"{total} F CFA")
            st.table(df_actuel[['nom', 'secteur', 'revenu']])
