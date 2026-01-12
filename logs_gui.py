import tkinter as tk
from tkinter import ttk
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "rfid_user",
    "password": "rfid123",
    "database": "rfid"
}

def carregar_logs():
    for item in tree.get_children():
        tree.delete(item)

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT uid, status, data_hora
            FROM logs
            ORDER BY data_hora DESC
            LIMIT 200
        """)

        for uid, status, data_hora in cursor.fetchall():
            tree.insert("", tk.END, values=(
                uid,
                status,
                data_hora.strftime("%d/%m/%Y %H:%M:%S")
            ))

        conn.close()
    except Exception as e:
        print("Erro ao carregar logs:", e)

def atualizar():
    carregar_logs()
    root.after(5000, atualizar)  # Atualiza a cada 5 segundos

# Janela principal
root = tk.Tk()
root.title("Logs de Acesso RFID")
root.geometry("600x400")

# Tabela
columns = ("UID", "Status", "Data e Hora")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=180)

tree.pack(fill=tk.BOTH, expand=True)

# Botão atualizar manual
btn = tk.Button(root, text="Atualizar agora", command=carregar_logs)
btn.pack(pady=5)

# Inicialização
carregar_logs()
atualizar()

root.mainloop()
