import serial
import time
import mysql.connector
from datetime import datetime
import keyboard

SERIAL_PORT = "COM6"
BAUDRATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

conn = mysql.connector.connect(
    host="localhost",
    user="rfid_user",
    password="rfid123",
    database="rfid"
)

cursor = conn.cursor()

print("Sistema iniciado.")
print("Passe o cartão para abrir.")
print("Pressione P para fechar a tranca.")

while True:
    # Fecha a tranca quando apertar P
    if keyboard.is_pressed("p"):
        print("Fechando tranca...")
        ser.write(b"CLOSE\n")
        while keyboard.is_pressed("p"):
            pass  # evita repetir várias vezes

    # Lê UID do Arduino
    linha = ser.readline().decode(errors="ignore").strip()
    if not linha:
        continue

    # Garante que é hexadecimal
    if not all(c in "0123456789ABCDEF" for c in linha.upper()):
        continue

    uid = linha.upper()
    print(f"UID recebido: {uid}")

    cursor.execute("SELECT nome FROM usuarios WHERE uid = %s", (uid,))
    result = cursor.fetchone()

    if result:
        nome = result[0]
        print(f"Acesso autorizado para {nome}")
        ser.write(b"OPEN\n")
    else:
        print("Acesso negado")