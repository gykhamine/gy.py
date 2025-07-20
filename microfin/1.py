import sqlite3
import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
from datetime import datetime
import tkinter.messagebox as mbox
import re
import datetime

class MicrofinDB:
    def __init__(self, db_name='microfin.db'):
        import os
        db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()
        self.create_tables()
        self.ensure_solde_column()
        self.create_connexion_table()
    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            telephone TEXT UNIQUE NOT NULL
        )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            montant REAL,
            type TEXT,
            date TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )''')
        self.conn.commit()
    def create_connexion_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS connexion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            heure TEXT
        )''')
        self.conn.commit()
    def ensure_solde_column(self):
        self.c.execute("PRAGMA table_info(clients)")
        columns = [col[1] for col in self.c.fetchall()]
        if 'solde' not in columns:
            self.c.execute('ALTER TABLE clients ADD COLUMN solde REAL DEFAULT 0')
            self.conn.commit()
    def add_client(self, nom, prenom, telephone):
        try:
            self.c.execute('INSERT INTO clients (nom, prenom, telephone, solde) VALUES (?, ?, ?, ?)', (nom, prenom, telephone, 0))
            self.conn.commit()
            return True, 'Client ajouté avec succès !'
        except sqlite3.IntegrityError:
            return False, 'Téléphone déjà utilisé !'
    def update_client(self, id, nom, prenom, telephone):
        self.c.execute('UPDATE clients SET nom=?, prenom=?, telephone=? WHERE id=?', (nom, prenom, telephone, id))
        self.conn.commit()
    def delete_client(self, id):
        self.c.execute('DELETE FROM clients WHERE id=?', (id,))
        self.conn.commit()
    def get_clients(self, search=None):
        if search:
            self.c.execute('SELECT id, nom, prenom, telephone, solde FROM clients WHERE nom LIKE ? OR telephone LIKE ?', (f'%{search}%', f'%{search}%'))
        else:
            self.c.execute('SELECT id, nom, prenom, telephone, solde FROM clients ORDER BY nom')
        return self.c.fetchall()
    def get_client(self, id):
        self.c.execute('SELECT id, nom, prenom, telephone, solde FROM clients WHERE id=?', (id,))
        return self.c.fetchone()
    def add_transaction(self, client_id, montant, type_):
        client = self.get_client(client_id)
        if not client:
            return False, 'Client introuvable !'
        solde = client[4]
        if type_ == 'Ajouter':
            nouveau_solde = solde + montant
        elif type_ == 'Retirer':
            if montant > solde:
                return False, 'Solde insuffisant !'
            nouveau_solde = solde - montant
        else:
            return False, 'Type de transaction invalide !'
        now = datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.c.execute('UPDATE clients SET solde=? WHERE id=?', (nouveau_solde, client_id))
        self.c.execute('INSERT INTO transactions (client_id, montant, type, date) VALUES (?, ?, ?, ?)', (client_id, montant, type_, date))
        self.conn.commit()
        return True, f'Transaction enregistrée ({date}) !'
    def get_transactions(self, client_id=None):
        if client_id:
            self.c.execute('SELECT t.id, c.nom, c.prenom, t.montant, t.type, t.date FROM transactions t JOIN clients c ON t.client_id = c.id WHERE c.id=? ORDER BY t.date DESC', (client_id,))
        else:
            self.c.execute('SELECT t.id, c.nom, c.prenom, t.montant, t.type, t.date FROM transactions t JOIN clients c ON t.client_id = c.id ORDER BY t.date DESC')
        return self.c.fetchall()
    def save_connexion(self):
        from datetime import datetime
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        heure = now.strftime('%H:%M:%S')
        self.c.execute('INSERT INTO connexion (date, heure) VALUES (?, ?)', (date, heure))
        self.conn.commit()
    def get_last_connexion(self):
        self.c.execute('SELECT date, heure FROM connexion ORDER BY id DESC LIMIT 1')
        return self.c.fetchone()

class MicrofinApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = MicrofinDB()
        self.title('Gestion Microfinance')
        self.geometry('700x500')
        self.check_system_time()
        self.create_widgets()
    def check_system_time(self):
        import datetime
        from tkinter import messagebox
        now = datetime.datetime.now()
        sys_date = now.strftime('%Y-%m-%d')
        sys_heure = now.strftime('%H:%M:%S')
        last = self.db.get_last_connexion()
        self.db.save_connexion()
        if last:
            last_date, last_heure = last
            if sys_date < last_date or (sys_date == last_date and sys_heure < last_heure):
                messagebox.showerror('Alerte système', 'La date ou l\'heure du système est incorrecte !\nAucune transaction ne sera possible.')
                self.transactions_disabled = True
            else:
                self.transactions_disabled = False
        else:
            self.transactions_disabled = False
    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        # Onglet Ajouter Client
        self.client_tab = self.tabview.add('Ajouter Client')
        self.client_frame = ctk.CTkFrame(self.client_tab, fg_color="#223322")
        self.client_frame.pack(pady=20, padx=20, fill='both', expand=True)
        self.client_frame.pack_propagate(0)
        # Champs en liste verticale
        self.nom_entry = ctk.CTkEntry(self.client_frame, placeholder_text='Nom')
        self.nom_entry.pack(fill='x', pady=2)
        self.prenom_entry = ctk.CTkEntry(self.client_frame, placeholder_text='Prénom')
        self.prenom_entry.pack(fill='x', pady=2)
        self.tel_entry = ctk.CTkEntry(self.client_frame, placeholder_text='Téléphone')
        self.tel_entry.pack(fill='x', pady=2)
        self.add_client_btn = ctk.CTkButton(self.client_frame, text='Ajouter', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.add_client)
        self.add_client_btn.pack(fill='x', pady=2)
        self.client_status = ctk.CTkLabel(self.client_tab, text='', text_color="#388e3c")
        self.client_status.pack(pady=5)
        # Onglet Modifier Client
        self.modify_tab = self.tabview.add('Modifier Client')
        self.modify_frame = ctk.CTkFrame(self.modify_tab, fg_color="#223322")
        self.modify_frame.pack(pady=20, padx=20, fill='both', expand=True)
        self.modify_frame.pack_propagate(0)
        self.modify_id_entry = ctk.CTkEntry(self.modify_frame, placeholder_text='ID du client à modifier')
        self.modify_id_entry.pack(fill='x', pady=2)
        self.modify_nom_entry = ctk.CTkEntry(self.modify_frame, placeholder_text='Nouveau nom')
        self.modify_nom_entry.pack(fill='x', pady=2)
        self.modify_prenom_entry = ctk.CTkEntry(self.modify_frame, placeholder_text='Nouveau prénom')
        self.modify_prenom_entry.pack(fill='x', pady=2)
        self.modify_tel_entry = ctk.CTkEntry(self.modify_frame, placeholder_text='Nouveau téléphone')
        self.modify_tel_entry.pack(fill='x', pady=2)
        self.modify_btn = ctk.CTkButton(self.modify_frame, text='Modifier', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.modify_client)
        self.modify_btn.pack(fill='x', pady=2)
        self.modify_status = ctk.CTkLabel(self.modify_tab, text='', text_color="#388e3c")
        self.modify_status.pack(pady=5)
        # Onglet Supprimer Client
        self.delete_tab = self.tabview.add('Supprimer Client')
        self.delete_frame = ctk.CTkFrame(self.delete_tab, fg_color="#223322")
        self.delete_frame.pack(pady=20, padx=20, fill='both', expand=True)
        self.delete_frame.pack_propagate(0)
        self.delete_client_id_entry = ctk.CTkEntry(self.delete_frame, placeholder_text='ID à supprimer')
        self.delete_client_id_entry.pack(fill='x', pady=2)
        self.delete_client_btn = ctk.CTkButton(self.delete_frame, text='Supprimer Client', fg_color="#d32f2f", hover_color="#c62828", text_color="white", command=self.delete_client)
        self.delete_client_btn.pack(fill='x', pady=2)
        self.delete_status = ctk.CTkLabel(self.delete_tab, text='', text_color="#d32f2f")
        self.delete_status.pack(pady=5)
        # Onglet Transactions
        self.trans_tab = self.tabview.add('Transactions')
        self.trans_frame = ctk.CTkFrame(self.trans_tab, fg_color="#223322")
        self.trans_frame.pack(pady=20, padx=20, fill='both', expand=True)
        self.trans_frame.pack_propagate(0)
        self.client_id_entry = ctk.CTkEntry(self.trans_frame, placeholder_text='ID Client')
        self.client_id_entry.pack(fill='x', pady=2)
        self.montant_entry = ctk.CTkEntry(self.trans_frame, placeholder_text='Montant')
        self.montant_entry.pack(fill='x', pady=2)
        self.type_option = ctk.CTkOptionMenu(self.trans_frame, values=['Ajouter', 'Retirer', 'Transférer'], command=self.toggle_benef_field)
        self.type_option.pack(fill='x', pady=2)
        self.benef_id_entry = ctk.CTkEntry(self.trans_frame, placeholder_text='ID bénéficiaire (pour transfert)')
        self.benef_id_entry.pack_forget()
        self.add_trans_btn = ctk.CTkButton(self.trans_frame, text='Enregistrer', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.add_transaction)
        self.add_trans_btn.pack(fill='x', pady=2)
        self.trans_status = ctk.CTkLabel(self.trans_tab, text='', text_color="#388e3c")
        self.trans_status.pack(pady=5)
        # Onglet Historique
        self.history_tab = self.tabview.add('Historique')
        self.history_frame = ctk.CTkFrame(self.history_tab, fg_color="#223322")
        self.history_frame.pack(pady=20, padx=20, fill='both', expand=True)
        self.history_frame.pack_propagate(0)
        self.filter_id_entry = ctk.CTkEntry(self.history_frame, placeholder_text='ID client')
        self.filter_id_entry.pack(fill='x', pady=2)
        # Listes préétablies pour jour, mois (lettres), année
        years = [str(y) for y in range(2025, 2036)]
        months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        days = [f'{d:02d}' for d in range(1, 32)]
        self.filter_year_option = ctk.CTkOptionMenu(self.history_frame, values=years)
        self.filter_year_option.pack(fill='x', pady=2)
        self.filter_month_option = ctk.CTkOptionMenu(self.history_frame, values=months)
        self.filter_month_option.pack(fill='x', pady=2)
        self.filter_day_option = ctk.CTkOptionMenu(self.history_frame, values=days)
        self.filter_day_option.pack(fill='x', pady=2)
        # Liste préétablie pour heure, minute, seconde
        hours = [f'{h:02d}' for h in range(0, 24)]
        minutes = [f'{m:02d}' for m in range(0, 60)]
        seconds = [f'{s:02d}' for s in range(0, 60)]
        self.filter_hour_option = ctk.CTkOptionMenu(self.history_frame, values=hours)
        self.filter_hour_option.pack(fill='x', pady=2)
        self.filter_minute_option = ctk.CTkOptionMenu(self.history_frame, values=minutes)
        self.filter_minute_option.pack(fill='x', pady=2)
        self.filter_second_option = ctk.CTkOptionMenu(self.history_frame, values=seconds)
        self.filter_second_option.pack(fill='x', pady=2)
        # Filtre par type
        self.filter_type_option = ctk.CTkOptionMenu(self.history_frame, values=['Tous', 'Ajouter', 'Retirer', 'Transférer', 'Transfert sortant', 'Transfert entrant'])
        self.filter_type_option.pack(fill='x', pady=2)
        self.filter_btn = ctk.CTkButton(self.history_frame, text='Filtrer', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.filter_history)
        self.filter_btn.pack(fill='x', pady=2)
        self.history_list = ctk.CTkTextbox(self.history_frame, width=650, height=250, fg_color="#263826", text_color="#c8e6c9")
        self.history_list.pack(fill='both', expand=True, pady=10)
        # Onglet Etat Système
        self.state_tab = self.tabview.add('Etat Système')
        self.state_frame = ctk.CTkFrame(self.state_tab, fg_color="#223322")
        self.state_frame.pack(pady=20, padx=20, fill='both', expand=True)
        self.state_frame.pack_propagate(0)
        self.state_label = ctk.CTkLabel(self.state_frame, text='', font=("Arial", 18), text_color="#388e3c")
        self.state_label.pack(fill='x', pady=10)
        self.update_state_tab()
        # Onglet Documentation
        self.doc_tab = self.tabview.add('Documentation')
        self.doc_frame = ctk.CTkFrame(self.doc_tab, fg_color="#223322")
        self.doc_frame.pack(pady=20, padx=20, fill='both', expand=True)
        self.doc_frame.pack_propagate(0)
        doc_text = (
            "Bienvenue dans le système de gestion de microfinance !\n\n"
            "Fonctionnalités principales :\n"
            "- Ajouter, modifier, supprimer un client\n"
            "- Gérer les transactions (dépôt, retrait, transfert)\n"
            "- Historique filtrable par date, heure, type, client\n"
            "- Blocage automatique des opérations si la date/heure système est incorrecte\n"
            "- Onglet Etat Système pour vérifier si les opérations sont autorisées\n\n"
            "Utilisation :\n"
            "1. Onglet 'Ajouter Client' : Remplissez les champs et cliquez sur Ajouter.\n"
            "2. Onglet 'Modifier Client' : Saisissez l'ID et les nouvelles infos, puis Modifier.\n"
            "3. Onglet 'Supprimer Client' : Saisissez l'ID et cliquez sur Supprimer.\n"
            "4. Onglet 'Transactions' : Saisissez l'ID client, le montant, le type et validez. Pour un transfert, indiquez aussi l'ID bénéficiaire.\n"
            "5. Onglet 'Historique' : Filtrez les transactions par client, date, heure, type.\n"
            "6. Onglet 'Etat Système' : Vérifiez si les opérations sont possibles.\n\n"
            "Règles et sécurité :\n"
            "- Les champs doivent être remplis correctement (nom/prénom en lettres, téléphone congolais, montant positif).\n"
            "- Les transactions sont bloquées si la date/heure système est incohérente.\n"
            "- La base de données est stockée dans le même dossier que le script.\n\n"
            "Pour toute question ou amélioration, contactez l'administrateur du système."
        )
        self.doc_box = ctk.CTkTextbox(self.doc_frame, width=650, height=400, fg_color="#263826", text_color="#c8e6c9")
        self.doc_box.pack(fill='both', expand=True, pady=10)
        self.doc_box.insert('end', doc_text)
        self.doc_box.configure(state='disabled')
    def add_client(self):
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        tel = self.tel_entry.get().strip()
        if not (nom and prenom and tel):
            self.client_status.configure(text='Veuillez remplir tous les champs pour ajouter un client.')
            return
        # Vérification Congo : nom et prénom non vides, texte uniquement
        if not nom or not prenom:
            self.client_status.configure(text='Nom et prénom obligatoires !')
            return
        if not nom.isalpha() or not prenom.isalpha():
            self.client_status.configure(text='Nom et prénom doivent être du texte (lettres uniquement) !')
            return
        # Format téléphone Congo : commence par 08, 09, 06, 07, 05, 04, 03, 02, 01, 099, 097, 089, 081, 082, 080, 090, 091, 092, 093, 094, 095, 096, 098, 083, 084, 085, 086, 087, 088, 08X, 09X, 06X, 07X, 05X, 04X, 03X, 02X, 01X, 099X, 097X, 089X, 081X, 082X, 080X, 090X, 091X, 092X, 093X, 094X, 095X, 096X, 098X, 083X, 084X, 085X, 086X, 087X, 088X
        if not re.match(r'^(0[89]|09|06|07|05|04|03|02|01)[0-9]{7,8}$', tel):
            self.client_status.configure(text='Téléphone congolais invalide !')
            return
        if not mbox.askyesno('Validation', f'Confirmer l\'ajout du client {nom} {prenom} ?'):
            self.client_status.configure(text='Ajout annulé.')
            return
        ok, msg = self.db.add_client(nom, prenom, tel)
        self.client_status.configure(text=msg)
        if ok:
            self.show_clients()
    def show_clients(self):
        self.client_list.delete('0.0', 'end')
        rows = self.db.get_clients()
        for row in row,s:
            self.client_list.insert('end', f'ID:{row[0]} | {row[1]} {row[2]} | Tel:{row[3]} | Solde:{row[4]}€\n')
    def search_client(self):
        query = self.search_entry.get()
        self.client_list.delete('0.0', 'end')
        rows = self.db.get_clients(search=query)
        for row in rows:
            self.client_list.insert('end', f'ID:{row[0]} | {row[1]} {row[2]} | Tel:{row[3]} | Solde:{row[4]}€\n')
    def delete_client(self):
        client_id = self.delete_client_id_entry.get().strip()
        if not client_id:
            self.delete_status.configure(text='Veuillez remplir le champ ID pour supprimer un client.')
            return
        if not mbox.askyesno('Validation', f'Confirmer la suppression du client ID {client_id} ?'):
            self.delete_status.configure(text='Suppression annulée.')
            return
        try:
            self.db.delete_client(client_id)
            self.delete_status.configure(text='Client supprimé !')
            self.show_clients()
        except Exception as e:
            self.delete_status.configure(text=f'Erreur suppression : {e}')
    def add_transaction(self):
        if hasattr(self, 'transactions_disabled') and self.transactions_disabled:
            self.trans_status.configure(text='Transactions désactivées : date/heure système incorrecte.')
            return
        client_id = self.client_id_entry.get().strip()
        montant = self.montant_entry.get().strip()
        type_ = self.type_option.get()
        benef_id = self.benef_id_entry.get().strip() if type_ == 'Transférer' else None
        if type_ == 'Transférer':
            if not (client_id and montant and benef_id):
                self.trans_status.configure(text='Veuillez remplir tous les champs pour le transfert.')
                return
        else:
            if not (client_id and montant):
                self.trans_status.configure(text='Veuillez remplir tous les champs pour la transaction.')
                return
        try:
            montant = float(montant)
        except ValueError:
            self.trans_status.configure(text='Montant invalide !')
            return
        if montant <= 0:
            self.trans_status.configure(text='Montant doit être positif !')
            return
        frais = 0
        # Gestion des frais (exemple : 1% sur transfert, 0.5% sur retrait)
        if type_ == 'Transférer':
            frais = round(montant * 0.01, 2)
        elif type_ == 'Retirer':
            frais = round(montant * 0.005, 2)
        montant_total = montant + frais if type_ in ['Transférer', 'Retirer'] else montant
        if not client_id.isdigit():
            self.trans_status.configure(text='ID client invalide !')
            return
        if type_ == 'Transférer':
            if not benef_id.isdigit():
                self.trans_status.configure(text='ID bénéficiaire invalide !')
                return
            if client_id == benef_id:
                self.trans_status.configure(text='Impossible de transférer à soi-même !')
                return
            if not mbox.askyesno('Validation', f'Confirmer le transfert de {montant}€ (+{frais}€ frais) du client {client_id} vers {benef_id} ?'):
                self.trans_status.configure(text='Transfert annulé.')
                return
            emetteur = self.db.get_client(client_id)
            beneficiaire = self.db.get_client(benef_id)
            if not emetteur or not beneficiaire:
                self.trans_status.configure(text='Client ou bénéficiaire introuvable !')
                return
            if montant_total > emetteur[4]:
                self.trans_status.configure(text='Solde insuffisant pour le transfert !')
                return
            self.db.add_transaction(client_id, montant_total, 'Transfert sortant')
            self.db.add_transaction(benef_id, montant, 'Transfert entrant')
            self.trans_status.configure(text=f'Transfert de {montant}€ effectué ! (frais {frais}€)')
            self.show_transactions()
            return
        if type_ == 'Retirer':
            if not mbox.askyesno('Validation', f'Confirmer le retrait de {montant}€ (+{frais}€ frais) pour le client ID {client_id} ?'):
                self.trans_status.configure(text='Retrait annulé.')
                return
            ok, msg = self.db.add_transaction(client_id, montant_total, type_)
            self.trans_status.configure(text=f'{msg} (frais {frais}€)')
            if ok:
                self.show_transactions()
            return
        if not mbox.askyesno('Validation', f'Confirmer la transaction {type_} de {montant}€ pour le client ID {client_id} ?'):
            self.trans_status.configure(text='Transaction annulée.')
            return
        ok, msg = self.db.add_transaction(client_id, montant, type_)
        self.trans_status.configure(text=msg)
        if ok:
            self.show_transactions()
    def show_transactions(self):
        self.trans_list.delete('0.0', 'end')
        rows = self.db.get_transactions()
        for row in rows:
            self.trans_list.insert('end', f'ID:{row[0]} | {row[1]} {row[2]} | {row[3]}€ | {row[4]} | {row[5]}\n')
    def modify_client(self):
        id = self.modify_id_entry.get().strip()
        nom = self.modify_nom_entry.get().strip()
        prenom = self.modify_prenom_entry.get().strip()
        tel = self.modify_tel_entry.get().strip()
        if not (id and nom and prenom and tel):
            self.modify_status.configure(text='Veuillez remplir tous les champs pour modifier un client.')
            return
        if not id.isdigit():
            self.modify_status.configure(text='ID client invalide !')
            return
        if not nom or not prenom:
            self.modify_status.configure(text='Nom et prénom obligatoires !')
            return
        if not nom.isalpha() or not prenom.isalpha():
            self.modify_status.configure(text='Nom et prénom doivent être du texte (lettres uniquement) !')
            return
        if not re.match(r'^(0[89]|09|06|07|05|04|03|02|01)[0-9]{7,8}$', tel):
            self.modify_status.configure(text='Téléphone congolais invalide !')
            return
        if not mbox.askyesno('Validation', f'Confirmer la modification du client ID {id} ?'):
            self.modify_status.configure(text='Modification annulée.')
            return
        try:
            self.db.update_client(id, nom, prenom, tel)
            self.modify_status.configure(text='Client modifié !')
            self.show_clients()
        except Exception as e:
            self.modify_status.configure(text=f'Erreur modification : {e}')
    def show_history(self):
        self.history_list.delete('0.0', 'end')
        rows = self.db.get_transactions()
        for row in rows:
            self.history_list.insert('end', f'ID:{row[0]} | {row[1]} {row[2]} | {row[3]}€ | {row[4]} | {row[5]}\n')
    def filter_history(self):
        self.history_list.delete('0.0', 'end')
        id_val = self.filter_id_entry.get().strip()
        year_val = self.filter_year_option.get()
        month_val = self.filter_month_option.get()
        day_val = self.filter_day_option.get()
        hour_val = self.filter_hour_option.get()
        minute_val = self.filter_minute_option.get()
        second_val = self.filter_second_option.get()
        type_val = self.filter_type_option.get()
        # Conversion mois lettre -> chiffre
        mois_map = {'Janvier':'01','Février':'02','Mars':'03','Avril':'04','Mai':'05','Juin':'06','Juillet':'07','Août':'08','Septembre':'09','Octobre':'10','Novembre':'11','Décembre':'12'}
        month_num = mois_map.get(month_val, '01')
        query = "SELECT t.id, c.nom, c.prenom, t.montant, t.type, t.date FROM transactions t JOIN clients c ON t.client_id = c.id WHERE 1=1"
        params = []
        if id_val:
            query += " AND c.id=?"
            params.append(id_val)
        if type_val and type_val != 'Tous':
            query += " AND t.type=?"
            params.append(type_val)
        # Filtre date
        date_filter = f'{year_val}-{month_num}-{day_val}'
        time_filter = f'{hour_val}:{minute_val}:{second_val}'
        if year_val and month_val and day_val and hour_val and minute_val and second_val:
            query += " AND t.date LIKE ?"
            params.append(f'{date_filter} {time_filter}%')
        elif year_val and month_val and day_val:
            query += " AND t.date LIKE ?"
            params.append(f'{date_filter}%')
        elif year_val and month_val:
            query += " AND t.date LIKE ?"
            params.append(f'{year_val}-{month_num}%')
        elif year_val:
            query += " AND t.date LIKE ?"
            params.append(f'{year_val}%')
        query += " ORDER BY t.type, t.date DESC"
        self.db.c.execute(query, tuple(params))
        rows = self.db.c.fetchall()
        if not rows:
            self.history_list.insert('end', 'Aucune transaction trouvée avec ces filtres.\n')
            return
        # Regroupement par type
        grouped = {}
        for row in rows:
            ttype = row[4]
            if ttype not in grouped:
                grouped[ttype] = []
            grouped[ttype].append(row)
        for ttype, items in grouped.items():
            self.history_list.insert('end', f'--- {ttype} ---\n')
            for row in items:
                self.history_list.insert('end', f'ID:{row[0]} | {row[1]} {row[2]} | {row[3]}€ | {row[5]}\n')
            self.history_list.insert('end', '\n')
    def toggle_benef_field(self, value):
        if value == 'Transférer':
            self.benef_id_entry.pack(fill='x', pady=2)
        else:
            self.benef_id_entry.pack_forget()
    def update_state_tab(self):
        last = self.db.get_last_connexion()
        import datetime
        now = datetime.datetime.now()
        sys_date = now.strftime('%Y-%m-%d')
        sys_heure = now.strftime('%H:%M:%S')
        if hasattr(self, 'transactions_disabled') and self.transactions_disabled:
            self.state_label.configure(text=f"Opérations BLOQUÉES !\nDate système : {sys_date}\nHeure système : {sys_heure}\nDernière connexion : {last[0]} {last[1]}", text_color="#d32f2f")
        else:
            self.state_label.configure(text=f"Opérations AUTORISÉES\nDate système : {sys_date}\nHeure système : {sys_heure}\nDernière connexion : {last[0]} {last[1]}", text_color="#388e3c")
    def on_closing(self):
        if mbox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application ?"):
            self.destroy()
    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        super().mainloop()

if __name__ == '__main__':
    app = MicrofinApp()
    app.run()
