import sqlite3
import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
from datetime import datetime
import tkinter.messagebox as mbox
import re

class MicrofinDB:
    def __init__(self, db_name='microfin.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_tables()
        self.ensure_solde_column()
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

class MicrofinApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = MicrofinDB()
        self.title('Gestion Microfinance')
        self.geometry('700x500')
        self.create_widgets()
    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        # Pour chaque frame, utiliser pack_propagate(0) et grid/sticky pour adapter la taille
        # Exemple pour le client_frame
        self.client_tab = self.tabview.add('Ajouter Client')
        self.client_frame = ctk.CTkFrame(self.client_tab, fg_color="#223322")
        self.client_frame.pack(pady=20, padx=20, fill='both', expand=True)
        self.client_frame.pack_propagate(0)
        for i in range(4):
            self.client_frame.grid_columnconfigure(i, weight=1)
        self.nom_entry = ctk.CTkEntry(self.client_frame, placeholder_text='Nom')
        self.nom_entry.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        self.prenom_entry = ctk.CTkEntry(self.client_frame, placeholder_text='Prénom')
        self.prenom_entry.grid(row=1, column=0, padx=0, pady=0, sticky="ew")
        self.tel_entry = ctk.CTkEntry(self.client_frame, placeholder_text='Téléphone')
        self.tel_entry.grid(row=2, column=0, padx=0, pady=0, sticky="ew")
        self.add_client_btn = ctk.CTkButton(self.client_frame, text='Ajouter', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.add_client)
        self.add_client_btn.grid(row=3, column=0, padx=0, pady=0, sticky="ew")
        self.client_status = ctk.CTkLabel(self.client_tab, text='', text_color="#388e3c")
        self.client_status.pack(pady=5)
        # Onglet Modifier Client
        self.modify_tab = self.tabview.add('Modifier Client')
        self.modify_frame = ctk.CTkFrame(self.modify_tab, fg_color="#223322")
        self.modify_frame.pack(pady=20, padx=20, fill='x')
        self.modify_id_entry = ctk.CTkEntry(self.modify_frame, placeholder_text='ID du client à modifier')
        self.modify_id_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.modify_nom_entry = ctk.CTkEntry(self.modify_frame, placeholder_text='Nouveau nom')
        self.modify_nom_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.modify_prenom_entry = ctk.CTkEntry(self.modify_frame, placeholder_text='Nouveau prénom')
        self.modify_prenom_entry.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.modify_tel_entry = ctk.CTkEntry(self.modify_frame, placeholder_text='Nouveau téléphone')
        self.modify_tel_entry.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        self.modify_btn = ctk.CTkButton(self.modify_frame, text='Modifier', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.modify_client)
        self.modify_btn.grid(row=0, column=4, padx=10, pady=10, sticky="ew")
        self.modify_status = ctk.CTkLabel(self.modify_tab, text='', text_color="#388e3c")
        self.modify_status.pack(pady=5)
        # Onglet Liste Clients
        self.list_tab = self.tabview.add('Liste Clients')
        self.client_list = ctk.CTkTextbox(self.list_tab, width=650, height=200, fg_color="#263826", text_color="#c8e6c9")
        self.client_list.pack(pady=20)
        self.refresh_client_btn = ctk.CTkButton(self.list_tab, text='Afficher Clients', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.show_clients)
        self.refresh_client_btn.pack(pady=5)
        self.search_entry = ctk.CTkEntry(self.list_tab, placeholder_text='Recherche par nom ou téléphone')
        self.search_entry.pack(pady=5)
        self.search_btn = ctk.CTkButton(self.list_tab, text='Rechercher', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.search_client)
        self.search_btn.pack(pady=5)
        # Onglet Supprimer Client
        self.delete_tab = self.tabview.add('Supprimer Client')
        self.delete_client_id_entry = ctk.CTkEntry(self.delete_tab, placeholder_text='ID à supprimer')
        self.delete_client_id_entry.pack(pady=20)
        self.delete_client_btn = ctk.CTkButton(self.delete_tab, text='Supprimer Client', fg_color="#d32f2f", hover_color="#c62828", text_color="white", command=self.delete_client)
        self.delete_client_btn.pack(pady=5)
        self.delete_status = ctk.CTkLabel(self.delete_tab, text='', text_color="#d32f2f")
        self.delete_status.pack(pady=5)
        # Onglet Transactions
        self.trans_tab = self.tabview.add('Transactions')
        self.trans_frame = ctk.CTkFrame(self.trans_tab, fg_color="#223322")
        self.trans_frame.pack(pady=20, padx=20, fill='x')
        self.client_id_entry = ctk.CTkEntry(self.trans_frame, placeholder_text='ID Client')
        self.client_id_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.montant_entry = ctk.CTkEntry(self.trans_frame, placeholder_text='Montant')
        self.montant_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.type_option = ctk.CTkOptionMenu(self.trans_frame, values=['Ajouter', 'Retirer', 'Transférer'], command=self.toggle_benef_field)
        self.type_option.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.add_trans_btn = ctk.CTkButton(self.trans_frame, text='Enregistrer', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.add_transaction)
        self.add_trans_btn.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        self.benef_id_entry = ctk.CTkEntry(self.trans_frame, placeholder_text='ID bénéficiaire (pour transfert)')
        self.benef_id_entry.grid_forget()
        self.trans_status = ctk.CTkLabel(self.trans_tab, text='', text_color="#388e3c")
        self.trans_status.pack(pady=5)
        self.trans_list = ctk.CTkTextbox(self.trans_tab, width=650, height=200, fg_color="#263826", text_color="#c8e6c9")
        self.trans_list.pack(pady=20)
        self.refresh_trans_btn = ctk.CTkButton(self.trans_tab, text='Afficher Transactions', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.show_transactions)
        self.refresh_trans_btn.pack(pady=5)
        # Onglet Historique
        self.history_tab = self.tabview.add('Historique')
        self.history_list = ctk.CTkTextbox(self.history_tab, width=650, height=300, fg_color="#263826", text_color="#c8e6c9")
        self.history_list.pack(pady=20)
        self.refresh_history_btn = ctk.CTkButton(self.history_tab, text='Afficher Historique', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.show_history)
        self.refresh_history_btn.pack(pady=5)
        self.filter_frame = ctk.CTkFrame(self.history_tab, fg_color="#223322")
        self.filter_frame.pack(pady=10, padx=10, fill='x')
        self.filter_id_entry = ctk.CTkEntry(self.filter_frame, placeholder_text='ID client')
        self.filter_id_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.filter_day_entry = ctk.CTkEntry(self.filter_frame, placeholder_text='Jour (AAAA-MM-JJ)')
        self.filter_day_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.filter_hour_entry = ctk.CTkEntry(self.filter_frame, placeholder_text='Heure (HH:MM)')
        self.filter_hour_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.filter_btn = ctk.CTkButton(self.filter_frame, text='Filtrer', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.filter_history)
        self.filter_btn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        # Onglet Recherche avancée
        self.advanced_filter_tab = self.tabview.add('Recherche avancée')
        self.adv_filter_frame = ctk.CTkFrame(self.advanced_filter_tab, fg_color="#223322")
        self.adv_filter_frame.pack(pady=10, padx=10, fill='x')
        self.adv_id_entry = ctk.CTkEntry(self.adv_filter_frame, placeholder_text='ID client')
        self.adv_id_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.adv_type_option = ctk.CTkOptionMenu(self.adv_filter_frame, values=['Tous', 'Ajouter', 'Retirer', 'Transférer', 'Transfert sortant', 'Transfert entrant'])
        self.adv_type_option.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.adv_min_entry = ctk.CTkEntry(self.adv_filter_frame, placeholder_text='Montant min')
        self.adv_min_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.adv_max_entry = ctk.CTkEntry(self.adv_filter_frame, placeholder_text='Montant max')
        self.adv_max_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.adv_day_entry = ctk.CTkEntry(self.adv_filter_frame, placeholder_text='Jour (AAAA-MM-JJ)')
        self.adv_day_entry.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        self.adv_btn = ctk.CTkButton(self.adv_filter_frame, text='Rechercher', fg_color="#388e3c", hover_color="#2e7d32", text_color="white", command=self.advanced_search)
        self.adv_btn.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        self.adv_list = ctk.CTkTextbox(self.advanced_filter_tab, width=650, height=250, fg_color="#263826", text_color="#c8e6c9")
        self.adv_list.pack(pady=20)
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
        for row in rows:
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
        day_val = self.filter_day_entry.get().strip()
        hour_val = self.filter_hour_entry.get().strip()
        query = "SELECT t.id, c.nom, c.prenom, t.montant, t.type, t.date FROM transactions t JOIN clients c ON t.client_id = c.id WHERE 1=1"
        params = []
        if id_val:
            query += " AND c.id=?"
            params.append(id_val)
        if day_val:
            query += " AND t.date LIKE ?"
            params.append(f'{day_val}%')
        if hour_val:
            query += " AND t.date LIKE ?"
            params.append(f'%{hour_val}%')
        query += " ORDER BY t.date DESC"
        self.db.c.execute(query, tuple(params))
        rows = self.db.c.fetchall()
        for row in rows:
            self.history_list.insert('end', f'ID:{row[0]} | {row[1]} {row[2]} | {row[3]}€ | {row[4]} | {row[5]}\n')
    def advanced_search(self):
        self.adv_list.delete('0.0', 'end')
        id_val = self.adv_id_entry.get().strip()
        type_val = self.adv_type_option.get()
        min_val = self.adv_min_entry.get().strip()
        max_val = self.adv_max_entry.get().strip()
        day_val = self.adv_day_entry.get().strip()
        # Empêcher la recherche si une information manque
        if not (id_val and type_val and min_val and max_val and day_val):
            self.adv_list.insert('end', 'Veuillez remplir tous les champs pour lancer la recherche avancée.\n')
            return
        query = "SELECT t.id, c.nom, c.prenom, t.montant, t.type, t.date FROM transactions t JOIN clients c ON t.client_id = c.id WHERE 1=1"
        params = []
        if id_val:
            query += " AND c.id=?"
            params.append(id_val)
        if type_val and type_val != 'Tous':
            query += " AND t.type=?"
            params.append(type_val)
        if min_val:
            query += " AND t.montant>=?"
            params.append(min_val)
        if max_val:
            query += " AND t.montant<=?"
            params.append(max_val)
        if day_val:
            query += " AND t.date LIKE ?"
            params.append(f'{day_val}%')
        query += " ORDER BY t.date DESC"
        self.db.c.execute(query, tuple(params))
        rows = self.db.c.fetchall()
        for row in rows:
            self.adv_list.insert('end', f'ID:{row[0]} | {row[1]} {row[2]} | {row[3]}€ | {row[4]} | {row[5]}\n')
    def toggle_benef_field(self, value):
        if value == 'Transférer':
            self.benef_id_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        else:
            self.benef_id_entry.grid_forget()

if __name__ == '__main__':
    app = MicrofinApp()
    app.mainloop()
