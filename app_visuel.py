import customtkinter as ctk
import webbrowser
import json
import os
import urllib.parse
from tkinter import messagebox, simpledialog

# --- STYLE ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

FICHIER_JSON = "salons_data.json"

class BeauteConnectBusiness(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Beauté Connect - Business Patron")
        self.geometry("550x900")
        
        self.salons = self.charger_donnees()
        self.code_admin = "0001"
        self.ville_actuelle = None
        
        self.ecran_accueil()

    def charger_donnees(self):
        if os.path.exists(FICHIER_JSON):
            with open(FICHIER_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"BOBO": {}, "OUAGA": {}}

    def sauvegarder(self):
        with open(FICHIER_JSON, "w", encoding="utf-8") as f:
            json.dump(self.salons, f, indent=4, ensure_ascii=False)

    def effacer(self):
        for w in self.winfo_children(): w.destroy()

    def ecran_accueil(self):
        self.effacer()
        # Calcul de tes gains totaux (toujours sur la base de 100F/resa)
        total = sum(s.get('gains', 0) for v in self.salons.values() for s in v.values())
        
        ctk.CTkLabel(self, text=f"MA CAISSE : {total} F CFA", font=("Helvetica", 28, "bold"), text_color="#FFD700").pack(pady=30)
        
        ctk.CTkButton(self, text="📍 BOBO-DIOULASSO", height=60, command=lambda: self.ecran_salons("BOBO")).pack(pady=10, padx=60, fill="x")
        ctk.CTkButton(self, text="📍 OUAGADOUGOU", height=60, command=lambda: self.ecran_salons("OUAGA")).pack(pady=10, padx=60, fill="x")
        
        ctk.CTkButton(self, text="+ ADMIN : PUBLIER SALON", fg_color="#E74C3C", command=self.verifier_admin).pack(pady=40)

    def verifier_admin(self):
        code = simpledialog.askstring("SÉCURITÉ", "Code Admin :", show='*')
        if code == self.code_admin: self.ecran_ajouter()

    def ecran_salons(self, ville):
        self.ville_actuelle = ville
        self.effacer()
        ctk.CTkLabel(self, text=f"ÉTABLISSEMENTS : {ville}", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        for nom, info in self.salons[ville].items():
            type_etab = info.get('type_etab', 'Salon')
            # On affiche tes gains par salon
            btn_text = f"✨ {nom} ({type_etab})\n📍 {info['quartier']} | 💰 Mes Gains : {info.get('gains', 0)}F"
            ctk.CTkButton(self, text=btn_text, height=85, fg_color="#2C3E50", 
                          command=lambda n=nom, i=info: self.ecran_details(n, i)).pack(pady=8, padx=60, fill="x")

        ctk.CTkButton(self, text="⬅️ Retour", command=self.ecran_accueil).pack(side="bottom", pady=20)

    def ecran_details(self, nom, info):
        self.effacer()
        ctk.CTkLabel(self, text=f"{info.get('type_etab', 'Salon')} : {nom}", font=("Helvetica", 22, "bold")).pack(pady=20)
        
        if info.get('photo'):
            ctk.CTkButton(self, text="📸 VOIR PHOTOS / RÉALISATIONS", fg_color="#3498DB", command=lambda: webbrowser.open(info['photo'])).pack(pady=5)

        nom_cl = ctk.CTkEntry(self, placeholder_text="Nom de la cliente", height=45)
        nom_cl.pack(pady=10, padx=60, fill="x")

        # Choix de la prestation
        ctk.CTkLabel(self, text="Choisir la prestation :").pack()
        type_presta = ctk.CTkSegmentedButton(self, values=["Coiffure Simple", "Mariage / Grand Événement 💍"])
        type_presta.set("Coiffure Simple")
        type_presta.pack(pady=10)

        jour_heure = ctk.CTkEntry(self, placeholder_text="Jour et Heure (ex: Samedi 10h)", height=45)
        jour_heure.pack(pady=10, padx=60, fill="x")

        def valider():
            if not nom_cl.get() or not jour_heure.get():
                messagebox.showwarning("Erreur", "Remplissez les informations !")
                return
            
            # --- LA RÈGLE D'OR DU PATRON : +100F ---
            self.salons[self.ville_actuelle][nom]['gains'] = self.salons[self.ville_actuelle][nom].get('gains', 0) + 100
            self.sauvegarder()

            # MESSAGE WHATSAPP PROFESSIONNEL
            presta = type_presta.get()
            texte = (f"Bonjour comment allez vous, je veux une réservation pour une {presta} "
                     f"le {jour_heure.get()} pour la cliente {nom_cl.get()} via Beauté Connect.")
            
            msg_url = urllib.parse.quote(texte)
            num = f"226{info['tel']}" if not info['tel'].startswith("226") else info['tel']
            
            webbrowser.open(f"https://wa.me/{num}?text={msg_url}")
            messagebox.showinfo("COMMISSION ENCAISSÉE", "Félicitations Patron !\nVous avez gagné 100 F sur cette mise en relation.")
            self.ecran_accueil()

        ctk.CTkButton(self, text="🚀 CONFIRMER RÉSERVATION (GAINS 100F)", fg_color="#27AE60", height=60, command=valider).pack(pady=20)
        ctk.CTkButton(self, text="⬅️ Retour", command=lambda: self.ecran_salons(self.ville_actuelle)).pack(side="bottom", pady=20)

    def ecran_ajouter(self):
        self.effacer()
        ctk.CTkLabel(self, text="ADMIN : ENREGISTRER PARTENAIRE", font=("Helvetica", 18, "bold")).pack(pady=15)
        
        v = ctk.CTkEntry(self, placeholder_text="Ville (BOBO/OUAGA)"); v.pack(pady=5, padx=60, fill="x")
        n = ctk.CTkEntry(self, placeholder_text="Nom du Salon"); n.pack(pady=5, padx=60, fill="x")
        
        ctk.CTkLabel(self, text="Type d'établissement :").pack()
        cat = ctk.CTkSegmentedButton(self, values=["Salon de Coiffure", "Institut de Beauté"])
        cat.set("Salon de Coiffure")
        cat.pack(pady=5)

        q = ctk.CTkEntry(self, placeholder_text="Quartier"); q.pack(pady=5, padx=60, fill="x")
        t = ctk.CTkEntry(self, placeholder_text="WhatsApp (ex: 70...)"); t.pack(pady=5, padx=60, fill="x")
        ph = ctk.CTkEntry(self, placeholder_text="Lien Photo (URL)"); ph.pack(pady=5, padx=60, fill="x")

        def save():
            ville = v.get().upper()
            if ville in self.salons and n.get():
                self.salons[ville][n.get()] = {
                    "tel": t.get(), "quartier": q.get(), "gains": 0, 
                    "photo": ph.get(), "type_etab": cat.get()
                }
                self.sauvegarder()
                messagebox.showinfo("OK", "Partenaire publié !")
                self.ecran_accueil()

        ctk.CTkButton(self, text="✅ PUBLIER", fg_color="#27AE60", height=50, command=save).pack(pady=20)
        ctk.CTkButton(self, text="Annuler", command=self.ecran_accueil).pack()

if __name__ == "__main__":
    app = BeauteConnectBusiness()
    app.mainloop()
