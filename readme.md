# 🔐 Sistema de Controle de Acesso RFID com Arduino, Python e MySQL

Este projeto implementa um sistema completo de controle de acesso utilizando RFID, Arduino, Servo Motor, Python e MySQL.  
Ele permite:

- Cadastro de usuários por UID de cartão RFID
- Abertura automática da tranca quando o acesso é autorizado
- Fechamento manual da tranca pressionando a tecla **P**
- Registro de todos os acessos em banco de dados
- Interface gráfica para cadastro de tags
- Interface gráfica para visualização dos logs em tempo real

É um sistema no padrão de soluções comerciais de controle de acesso.

---

## 🧩 Arquitetura do Sistema
[Cartão RFID]
↓
[Arduino + MFRC522] → Serial → [Python]
↓
[MySQL]
↓
[Interfaces Gráficas]



Componentes:

- Arduino:
  - Leitura do cartão RFID
  - Controle do servo motor (tranca)
  - Comunicação serial com o computador

- Python:
  - Serviço de autenticação (`rfid_service.py`)
  - Tela de cadastro de tags (`cadastrar_gui.py`)
  - Tela de logs (`logs_gui.py`)

- MySQL:
  - Armazena usuários autorizados
  - Armazena histórico de acessos

---

## 🛠️ Requisitos

### Hardware
- Arduino Uno (ou compatível)
- Leitor RFID MFRC522
- Servo motor SG90
- Cartões ou tags RFID
- Jumpers e fonte adequada para o servo

### Software
- Python 3.10+
- MySQL (ou MySQL em container Docker)
- Bibliotecas Python:
```bash
pip install pyserial mysql-connector-python tkinter keyboard
```

🗄️ Estrutura do Banco de Dados
Banco: rfid

Tabela de usuários:
```bash
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    uid VARCHAR(50) NOT NULL UNIQUE
);
```
```bash
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uid VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    data_hora DATETIME NOT NULL
);
```

📁 Estrutura do Projeto

RFID_PROJECT/
│
├── arduino/
│   └── rfid_servo.ino
│
├── cadastrar_gui.py     # Tela para cadastrar cartões RFID
├── rfid_service.py      # Serviço principal de autenticação e controle do servo
├── logs_gui.py          # Tela para visualização dos logs
├── create_db.py         # Script para criar o banco e as tabelas
└── README.md

▶️ Como Executar
1. Suba seu MySQL (local ou via Docker)

2. Crie o banco usando:
```bash
python create_db.py
```

3. Suba o código no Arduino:

---Configure os pinos:
--RFID:
-SS → 10
-RST → 5

--Servo:
-Sinal → 3

Execute a tela de cadastro:
```bash
python cadastrar_gui.py
```
Digite a senha master
Aproxime a tag
Informe o nome do usuário

5. Inicie o sistema principal:
```bash
python rfid_service.py
```

Mensagem Exibida:

Sistema iniciado.
Passe o cartão para abrir.
Pressione P para fechar a tranca.

6. Visualize os logs:
```bash
python logs_gui.py
```

🔁 Funcionamento do Fluxo

1. Usuário aproxima a tag
2. Arduino envia UID pela serial
3. Python consulta o MySQL
4. Se autorizado:
5. Servo gira → tranca abre
6. Log: Acesso autorizado
--Se negado:
Servo não se move
Log: Acesso negado
--Pressionando P:
Servo retorna → tranca fecha

🚀 Evoluções Futuras

Controle de múltiplos níveis de acesso

Cadastro de senha por usuário

Interface Web

Dashboard com estatísticas

Integração com câmeras ou sensores

📜 Licença
Este projeto é de uso livre para fins educacionais, acadêmicos e experimentais.