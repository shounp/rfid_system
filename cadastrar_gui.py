import tkinter as tk
from tkinter import messagebox
import serial
from database import SessionLocal
from models import Usuario

# =========================
# CONFIGURAÇÕES
# =========================
SERIAL_PORT = "COM6"
BAUDRATE = 9600

SENHA_MASTER = "1234"   # depois você pode colocar em variável de ambiente

# =========================
# CONEXÕES
# =========================
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
session = SessionLocal()

# =========================
# FUNÇÕES
# =========================
def autenticar():
    senha = entry_senha.get()
    if senha == SENHA_MASTER:
        messagebox.showinfo("Sucesso", "Senha master correta.\nAproxime a tag RFID.")
        status_label.config(text="Aguardando leitura da tag RFID...")
        root.after(100, ler_uid)
    else:
        messagebox.showerror("Erro", "Senha master incorreta!")


def ler_uid():
    uid = ser.readline().decode().strip()

    if not uid:
        root.after(100, ler_uid)
        return

    entry_uid.delete(0, tk.END)
    entry_uid.insert(0, uid)
    status_label.config(text=f"UID lido: {uid}")


def cadastrar():
    uid = entry_uid.get().strip()
    nome = entry_nome.get().strip()

    if not uid or not nome:
        messagebox.showerror("Erro", "UID e Nome são obrigatórios!")
        return

    existe = session.query(Usuario).filter_by(uid=uid).first()
    if existe:
        messagebox.showwarning("Aviso", "Este UID já está cadastrado!")
        return

    novo = Usuario(uid=uid, nome=nome)
    session.add(novo)
    session.commit()

    messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado com sucesso!")
    status_label.config(text="Cadastro concluído. Pronto para novo cadastro.")

    entry_uid.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_senha.delete(0, tk.END)


# =========================
# INTERFACE
# =========================
root = tk.Tk()
root.title("Cadastro de Tag RFID - Acesso Master")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Senha Master:").pack(pady=5)
entry_senha = tk.Entry(root, show="*")
entry_senha.pack()

btn_auth = tk.Button(root, text="Autenticar", command=autenticar)
btn_auth.pack(pady=10)

tk.Label(root, text="UID da Tag:").pack()
entry_uid = tk.Entry(root, width=40)
entry_uid.pack()

tk.Label(root, text="Nome do Usuário:").pack()
entry_nome = tk.Entry(root, width=40)
entry_nome.pack()

btn_cadastrar = tk.Button(root, text="Cadastrar Usuário", command=cadastrar)
btn_cadastrar.pack(pady=15)

status_label = tk.Label(root, text="Informe a senha master para iniciar.")
status_label.pack(pady=10)

root.mainloop()
