from database import session, Login


def listar_utilizadores():
    utilizadores = session.query(Login).all()

    if not utilizadores:
        print("Não existem utilizadores na base de dados.")
        return

    print(f"Total de utilizadores: {len(utilizadores)}\n")
    for user in utilizadores:
        print(f"ID: {user.id}")
        print(f"Utilizador (username): {user.username}")
        print(f"Password: {user.password}")
        print("-" * 40)


if __name__ == "__main__":
    listar_utilizadores()

