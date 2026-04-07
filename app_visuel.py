import customtkinter as ctk
import webbrowser
import json
import os
import urllib.parse
from tkinter import messagebox, simpledialog

# --- STYLE PREMIUM ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

FICHIER_JSON = "salons_data_final.json"

class BeauteConnectBurkinaElite(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Beauté Connect - Système Expert Burkina")
        self.geometry("600x950")
        
        self.salons = self.charger_donnees()
        self.code_admin = "0001"
        self.ville_actuelle = None
        self.ecran_accueil()

    def charger_donnees(self):
        if os.path.exists(FICHIER_JSON):
            with open(FICHIER_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        # Base vide pour tes deux villes
        return {"BOBO": {}, "OUAGA": {}}

    def sauvegarder(self):
        with open(FICHIER_JSON, "w", encoding="utf-8") as f:
            json.dump(self.salons, f, indent=4, ensure_ascii=False)

    def effacer(self):
        for w in self.winfo_children(): w.destroy()

    def ecran_accueil(self):
        self.effacer()
        total = sum(s.get('gains', 0) for v in self.salons.values() for s in v.values())
        ctk.CTkLabel(self, text="✨ BEAUTÉ CONNECT ✨", font=("Helvetica", 26, "bold"), text_color="#FFD700").pack(pady=20)
        ctk.CTkLabel(self, text=f"💰 CAISSE PATRON : {total} F CFA", font=("Helvetica", 24, "bold"), text_color="#27AE60").pack(pady=10)
        
        ctk.CTkButton(self, text="📍 BOBO-DIOULASSO (Secteurs 1-25)", height=65, command=lambda: self.ecran_salons("BOBO")).pack(pady=15, padx=60, fill="x")
        ctk.CTkButton(self, text="📍 OUAGADOUGOU (Quartiers Top 30)", height=65, command=lambda: self.ecran_salons("OUAGA")).pack(pady=15, padx=60, fill="x")
        
        ctk.CTkButton(self, text="+ ADMIN : PUBLIER UN PARTENAIRE", fg_color="#E74C3C", command=self.verifier_admin).pack(pady=50)

    def verifier_admin(self):
        code = simpledialog.askstring("SÉCURITÉ", "Code Admin (0001) :", show='*')
        if code == self.code_admin: self.ecran_ajouter()

    def ecran_salons(self, ville):
        self.ville_actuelle = ville
        self.effacer()
        ctk.CTkLabel(self, text=f"PARTENAIRES : {ville}", font=("Helvetica", 20, "bold")).pack(pady=25)
        
        if not self.salons[ville]:
            ctk.CTkLabel(self, text="Aucun salon enregistré.", text_color="gray").pack(pady=50)
        else:
            for nom, info in self.salons[ville].items():
                cat = info.get('categorie', 'Salon')
                btn_text = f"✨ {nom} ({cat})\n📍 {info['quartier']} | 💵 Gains : {info.get('gains', 0)}F"
                ctk.CTkButton(self, text=btn_text, height=90, fg_color="#2C3E50", 
                              command=lambda n=nom, i=info: self.ecran_details(n, i)).pack(pady=8, padx=60, fill="x")

        ctk.CTkButton(self, text="⬅️ Retour", command=self.ecran_accueil).pack(side="bottom", pady=20)

    def ecran_details(self, nom, info):
        self.effacer()
        ctk.CTkLabel(self, text=f"{info.get('categorie', 'Salon')} : {nom}", font=("Helvetica", 22, "bold")).pack(pady=20)
        
        if info.get('photo'):
            ctk.CTkButton(self, text="📸 VOIR PHOTOS", fg_color="#3498DB", command=lambda: webbrowser.open(info['photo'])).pack(pady=5)

        nom_cl = ctk.CTkEntry(self, placeholder_text="Nom de la cliente", height=45)
        nom_cl.pack(pady=10, padx=60, fill="x")

        type_presta = ctk.CTkSegmentedButton(self, values=["Simple", "Mariage 💍 / Event"])
        type_presta.set("Simple")
        type_presta.pack(pady=10)

        jour_heure = ctk.CTkEntry(self, placeholder_text="Jour et Heure (ex: Samedi 10h)", height=45)
        jour_heure.pack(pady=10, padx=60, fill="x")

        def valider():
            if not nom_cl.get() or not jour_heure.get(): return
            
            # --- LES 100 F DU PATRON ---
            self.salons[self.ville_actuelle][nom]['gains'] = self.salons[self.ville_actuelle][nom].get('gains', 0) + 100
            self.sauvegarder()

            # Message WhatsApp Royal (Identique pour toutes les villes)
            texte = (f"Bonjour comment allez vous, je veux une réservation pour une {type_presta.get()} "
                     f"le {jour_heure.get()} pour la cliente {nom_cl.get()} via Beauté Connect.")
            
            msg_url = urllib.parse.quote(texte)
            num_brut = info['tel'].replace(" ", "").replace("+", "")
            num_final = f"226{num_brut}" if not num_brut.startswith("226") else num_brut
            
            webbrowser.open(f"https://wa.me/{num_final}?text={msg_url}")
            messagebox.showinfo("RECU", "100 F ajoutés à la caisse !")
            self.ecran_accueil()

        ctk.CTkButton(self, text="🚀 CONFIRMER & GAGNER 100F", fg_color="#27AE60", height=65, command=valider).pack(pady=30)
        ctk.CTkButton(self, text="⬅️ Retour", command=lambda: self.ecran_salons(self.ville_actuelle)).pack(side="bottom", pady=20)

    def ecran_ajouter(self):
        self.effacer()
        ctk.CTkLabel(self, text="PUBLIER UN NOUVEAU PARTENAIRE", font=("Helvetica", 18, "bold")).pack(pady=15)
        
        v = ctk.CTkEntry(self, placeholder_text="Ville (BOBO ou OUAGA)"); v.pack(pady=5, padx=60, fill="x")
        n = ctk.CTkEntry(self, placeholder_text="Nom de l'établissement"); n.pack(pady=5, padx=60, fill="x")
        
        ctk.CTkLabel(self, text="Catégorie :").pack()
        cat = ctk.CTkSegmentedButton(self, values=["Salon de Coiffure", "Institut de Beauté"])
        cat.set("Salon de Coiffure")
        cat.pack(pady=5)

        q = ctk.CTkEntry(self, placeholder_text="Quartier / Secteur (Karpala, Secteur 10...)"); q.pack(pady=5, padx=60, fill="x")
        t = ctk.CTkEntry(self, placeholder_text="Numéro WhatsApp"); t.pack(pady=5, padx=60, fill="x")
        ph = ctk.CTkEntry(self, placeholder_text="Lien Photo URL (i.ibb.co)"); ph.pack(pady=5, padx=60, fill="x")

        def save():
            ville = v.get().upper()
            if ville in self.salons and n.get():
                self.salons[ville][n.get()] = {
                    "tel": t.get(), "quartier": q.get(), "gains": 0, 
                    "categorie": cat.get(), "photo": ph.get()
                }
                self.sauvegarder()
                messagebox.showinfo("Succès", "Publication réussie !")
                self.ecran_accueil()

        ctk.CTkButton(self, text="✅ PUBLIER MAINTENANT", fg_color="#27AE60", height=55, command=save).pack(pady=30)
        ctk.CTkButton(self, text="Annuler", command=self.ecran_accueil).pack()

if __name__ == "__main__":
    app = BeauteConnectBurkinaElite()
    app.mainloop()
