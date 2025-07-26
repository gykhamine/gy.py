import customtkinter as ctk
import tkinter as tk

# Liste complète des registres x86-64 et leurs descriptions
registers = {
    "RAX": "Registre accumulateur, utilisé pour les opérations arithmétiques.",
    "RBX": "Registre de base, utilisé pour stocker des données temporaires.",
    "RCX": "Registre de compteur, utilisé dans les boucles ou pour stocker l'argument 4.",
    "RDX": "Registre de données, utilisé pour stocker des données temporaires ou l'argument 3.",
    "RSI": "Registre source index, utilisé pour les opérations de chaîne et l'argument 2.",
    "RDI": "Registre destination index, utilisé pour les opérations de chaîne et l'argument 1.",
    "RBP": "Base pointer, utilisé pour gérer la pile.",
    "RSP": "Stack pointer, pointe vers le sommet de la pile.",
    "R8": "Registre supplémentaire pour les arguments.",
    "R9": "Registre supplémentaire pour les arguments.",
    "R10": "Registre temporaire, utilisé par l'appelant.",
    "R11": "Registre temporaire, utilisé par l'appelant.",
    "R12": "Registre callee-saved, utilisé pour stocker des variables locales.",
    "R13": "Registre callee-saved, utilisé pour stocker des variables locales.",
    "R14": "Registre callee-saved, utilisé pour stocker des variables locales.",
    "R15": "Registre callee-saved, utilisé pour stocker des variables locales.",
    "RIP": "Instruction pointer, pointe vers l'instruction en cours.",
    "RFLAGS": "Registre de statut, contenant des flags comme le Zero Flag (ZF), le Carry Flag (CF), etc.",
    "CS": "Registre de segment code, utilisé pour accéder au code du programme.",
    "DS": "Registre de segment data, utilisé pour accéder aux données.",
    "ES": "Registre de segment extra, utilisé pour les chaînes.",
    "FS": "Registre de segment, utilisé pour accéder à des structures spécifiques au système.",
    "GS": "Registre de segment, utilisé pour des fonctions système.",
    "SS": "Registre de segment stack, utilisé pour accéder à la pile.",
    "R8D": "Les 32 premiers bits de R8.",
    "R9D": "Les 32 premiers bits de R9.",
    "R10D": "Les 32 premiers bits de R10.",
    "R11D": "Les 32 premiers bits de R11.",
    "R12D": "Les 32 premiers bits de R12.",
    "R13D": "Les 32 premiers bits de R13.",
    "R14D": "Les 32 premiers bits de R14.",
    "R15D": "Les 32 premiers bits de R15.",
    "AH": "Le byte le plus significatif de AX, utilisé dans certaines opérations arithmétiques.",
    "AL": "Le byte le moins significatif de AX, utilisé dans des opérations spécifiques.",
    "BH": "Le byte le plus significatif de BX.",
    "BL": "Le byte le moins significatif de BX.",
    "CH": "Le byte le plus significatif de CX.",
    "CL": "Le byte le moins significatif de CX.",
    "DH": "Le byte le plus significatif de DX.",
    "DL": "Le byte le moins significatif de DX.",
    "SREG": "Registres de segments supplémentaires, utilisés pour des segments spécifiques en mode protégé."
}

# Liste complète des instructions x86-64 et leurs explications en français
instructions = {
    "MOV": "Déplace des données d'un registre à un autre ou dans la mémoire.",
    "ADD": "Additionne deux valeurs.",
    "SUB": "Soustrait deux valeurs.",
    "MUL": "Effectue une multiplication non signée.",
    "IMUL": "Effectue une multiplication signée.",
    "DIV": "Effectue une division non signée.",
    "IDIV": "Effectue une division signée.",
    "PUSH": "Empile une valeur sur la pile.",
    "POP": "Dépile une valeur de la pile.",
    "CALL": "Appelle une fonction.",
    "RET": "Retourne d'une fonction.",
    "JMP": "Effectue un saut inconditionnel.",
    "JE": "Effectue un saut si l'égalité (ZF = 1).",
    "JNE": "Effectue un saut si la différence (ZF = 0).",
    "JG": "Effectue un saut si supérieur (ZF = 0, SF = OF).",
    "JL": "Effectue un saut si inférieur (SF ≠ OF).",
    "JGE": "Effectue un saut si supérieur ou égal (SF = OF).",
    "JLE": "Effectue un saut si inférieur ou égal (ZF = 1 ou SF ≠ OF).",
    "NOP": "Aucune opération, utilisée pour l'alignement ou pour ajouter du délai.",
    "XOR": "Effectue une opération logique XOR sur deux opérandes.",
    "AND": "Effectue une opération logique AND sur deux opérandes.",
    "OR": "Effectue une opération logique OR sur deux opérandes.",
    "NOT": "Inverse tous les bits d'un opérande.",
    "CMP": "Compare deux valeurs (effectue une soustraction mais ne stocke pas le résultat).",
    "TEST": "Effectue une opération AND entre deux opérandes et met à jour les flags.",
    "LEA": "Charge l'adresse effective dans un registre.",
    "INC": "Incrémente une valeur.",
    "DEC": "Décrémente une valeur.",
    "SAR": "Effectue une rotation arithmétique à droite.",
    "SHR": "Effectue une rotation logique à droite.",
    "SHL": "Effectue une rotation logique à gauche.",
    "ROL": "Effectue une rotation à gauche (avec retour du bit le plus significatif).",
    "ROR": "Effectue une rotation à droite (avec retour du bit le moins significatif).",
    "SETE": "Mets à 1 le registre si l'égalité est vraie (ZF = 1).",
    "SETNE": "Mets à 1 le registre si l'inégalité est vraie (ZF = 0).",
    "CMOV": "Effectue un mouvement conditionnel basé sur les flags.",
    "PUSHF": "Pousse le registre de flags sur la pile.",
    "POPF": "Dépile le registre de flags de la pile.",
    "CLC": "Efface le Carry Flag (CF).",
    "STC": "Mets le Carry Flag (CF) à 1.",
    "CLD": "Efface le Direction Flag (DF).",
    "STD": "Mets le Direction Flag (DF) à 1.",
    "RDTSC": "Lire le Time Stamp Counter (compteur de cycles CPU).",
    "CPUID": "Effectue une instruction de contrôle du processeur.",
    "RDRAND": "Génère un nombre aléatoire à l'aide du processeur.",
    "CLFLUSH": "Efface un cache de ligne pour une adresse mémoire donnée.",
    "MOVSX": "Déplace avec extension de signe (sign extension).",
    "MOVZX": "Déplace avec extension de zéro (zero extension).",
    "FADD": "Additionne deux nombres en virgule flottante.",
    "FSQRT": "Calcule la racine carrée d'un nombre en virgule flottante.",
    "FMUL": "Multiplie deux nombres en virgule flottante.",
    "FDIV": "Divise deux nombres en virgule flottante.",
    "FLD": "Charge une valeur en mémoire dans le registre de la FPU.",
    "FST": "Stocke une valeur de la FPU dans la mémoire.",
    "FCOM": "Compare une valeur FPU avec une autre valeur FPU.",
    "FSUB": "Soustrait une valeur FPU d'une autre.",
    "FSUBR": "Soustrait une valeur FPU d'une autre (ordre inverse).",
    "FDIVR": "Divise une valeur FPU par une autre (ordre inverse).",
    "FDIV": "Divise une valeur FPU par une autre.",
    "FINIT": "Initialise les registres FPU.",
    "FSAVE": "Sauvegarde l'état de la FPU.",
    "FRSTOR": "Restaure l'état de la FPU.",
    "FLD1": "Charge la constante 1 dans un registre FPU.",
    "FLDZ": "Charge la constante 0 dans un registre FPU.",
    "F2XM1": "Calcule 2^x - 1.",
    "FABS": "Prend la valeur absolue d'un nombre en FPU.",
    "FSCALE": "Multiplie un nombre en FPU par une puissance de 2.",
    "LDS": "Charge un segment de données et un pointeur.",
    "LES": "Charge un segment et un pointeur.",
    "LFS": "Charge un segment de données et un pointeur.",
    "LGS": "Charge un segment de données et un pointeur."
}

def build_listbox(frame, data):
    lb = tk.Listbox(frame, width=40, font=("Consolas", 12))
    for key in data:
        lb.insert(tk.END, key)
    lb.pack(side="left", fill="y", padx=(5,0), pady=5)
    sb = tk.Scrollbar(frame, orient="vertical", command=lb.yview)
    sb.pack(side="left", fill="y")
    lb.config(yscrollcommand=sb.set)
    return lb

def setup_gui():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = ctk.CTk()
    app.title("Registres et Instructions x86-64")

    # Frames
    frame_left = ctk.CTkFrame(app, width=250, height=400)
    frame_right = ctk.CTkFrame(app, width=600, height=400)
    frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
    frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    app.grid_columnconfigure(1, weight=1)

    # Listboxes pour les registres et instructions
    lb_regs = build_listbox(frame_left, registers)
    lb_instr = build_listbox(frame_left, instructions)

    # Zone de texte pour afficher la description
    txt = ctk.CTkTextbox(frame_right, width=600, height=400)
    txt.pack(expand=True, fill="both", padx=5, pady=5)

    def show_desc(event):
        sel = event.widget.get(event.widget.curselection())
        if event.widget == lb_regs:
            desc = registers[sel]
        else:
            desc = instructions[sel]
        txt.delete("0.0", tk.END)
        txt.insert(tk.END, f"{sel}:\n{desc}")

    lb_regs.bind("<<ListboxSelect>>", show_desc)
    lb_instr.bind("<<ListboxSelect>>", show_desc)

    app.mainloop()

if __name__ == "__main__":
    setup_gui()
