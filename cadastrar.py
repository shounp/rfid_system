from database import SessionLocal
from models import Usuario

def main():
    session = SessionLocal()

    uid = input("Digite o UID da tag: ").strip()
    nome = input("Digite o nome do usuário: ").strip()

    existe = session.query(Usuario).filter_by(uid=uid).first()
    if existe:
        print("Este UID já está cadastrado!")
        return

    novo = Usuario(uid=uid, nome=nome)
    session.add(novo)
    session.commit()

    print("Usuário cadastrado com sucesso!")

if __name__ == "__main__":
    main()
