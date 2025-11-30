import redis
import random
from datetime import date, datetime, timedelta

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def add_player(id, name, country, score):
    r.hset(f"player:{id}", mapping={
        "name": name,
        "country": country,
        "games_played": 0,
        "score": score
    })
    r.zadd("leaderboard", {id: score})

def update_score(id, points):
    key = f"player:{id}"
    if not r.exists(key):
        print("Jugador no encontrado")
        return
    new_score = r.hincrby(key, "score", points)
    r.hincrby(key, "games_played", 1)
    r.zadd("leaderboard", {id: new_score})
    return new_score

def player_info(id):
    key = f"player:{id}"
    if not r.exists(key):
        return None
    return r.hgetall(key)

def show_top_players(n):
    top = r.zrevrange("leaderboard", 0, n-1, withscores=True)
    result = []
    for pid, score in top:
        info = r.hgetall(f"player:{pid}")
        result.append((pid, info.get("name"), info.get("country"), int(score)))
    return result


def register_login(player_id):
    today = date.today().isoformat()
    r.pfadd(f"unique:players:{today}", player_id)

def count_unique_logins(date_str):
    return r.pfcount(f"unique:players:{date_str}")

def weekly_report(dates):
    keys = [f"unique:players:{d}" for d in dates]
    r.pfmerge("unique:players:week", *keys)
    return r.pfcount("unique:players:week")

def reset_system():
    r.flushdb()

def cargar_datos():
    print("Cargando datos de prueba...")
    nombres = [
        ("Severus", "Terra"),
        ("Valeria", "Cadia"),
        ("Mordecai", "Armageddon"),
        ("Lucius", "Fenris"),
        ("Astra", "Nocturne"),
        ("Helbrecht", "Macragge"),
        ("Kyria", "Baal"),
        ("Tiberius", "Prospero"),
        ("Galen", "Calth"),
        ("Seraphine", "Tanith"),
        ("Varex", "Necromunda"),
        ("Cassia", "Vigilus"),
        ("Thaddeus", "Krieg"),
        ("Aquila", "Tallarn"),
        ("Dominus", "Mortis Prime"),
        ("Iskander", "Holy Terra"),
        ("Selene", "Chogoris"),
        ("Varian", "Olympia"),
        ("Helia", "Armatura"),
        ("Kastor", "Caliban")
    ]


    for i, (nombre, mundo) in enumerate(nombres, start=1):
        score = random.randint(500, 2000)
        add_player(i, nombre, mundo, score)

    print("20 jugadores creados.")


    print("Aplicando actualizaciones de puntuación...")

    for _ in range(200):  # 200 partidas simuladas
        player_id = random.randint(1, 20)
        puntos = random.randint(-50, 200) 
        update_score(player_id, puntos)

    print("Actualizaciones completadas.")

    print("Registrando logins del mes de noviembre 2025...")

    start = datetime(2025, 11, 1)
    end = datetime(2025, 11, 26)

    day = start
    while day <= end:
        key = f"unique:players:{day.date().isoformat()}"
        
        # Cada día se conectan entre 10 y 20 jugadores
        num_logins = random.randint(10, 20)
        for _ in range(num_logins):
            player_id = random.randint(1, 20)
            r.pfadd(key, player_id)
        
        day += timedelta(days=1)

    print("Logins de noviembre registrados correctamente.")

def menu():
    while True:
        print("\n=== MENÚ TORNEO ONLINE ===")
        print("1. Agregar jugador")
        print("2. Actualizar puntuación")
        print("3. Ver info de un jugador")
        print("4. Mostrar top N")
        print("5. Registrar login")
        print("6. Ver logins únicos por fecha")
        print("7. Informe semanal")
        print("8. Resetear sistema")
        print("9. Cargar datos de prueba")
        print("0. Salir")

        op = input("Opción: ")

        if op == "1":
            id_ = int(input("ID: "))
            name = input("Nombre: ")
            country = input("País: ")
            score = int(input("Puntuación inicial: "))
            add_player(id_, name, country, score)
            print("Jugador añadido.")

        elif op == "2":
            id_ = int(input("ID: "))
            pts = int(input("Puntos a sumar: "))
            new = update_score(id_, pts)
            print("Nuevo score:", new)

        elif op == "3":
            id_ = int(input("ID: "))
            print(player_info(id_))

        elif op == "4":
            n = int(input("¿Cuántos?: "))
            for p in show_top_players(n):
                print(p)

        elif op == "5":
            id_ = int(input("ID jugador: "))
            register_login(id_)
            print("Login registrado.")

        elif op == "6":
            d = input("Fecha (YYYY-MM-DD): ")
            print("Únicos:", count_unique_logins(d))

        elif op == "7":
            fechas = input("Fechas separadas por comas: ").split(",")
            fechas = [f.strip() for f in fechas]
            print("Total sem semanal:", weekly_report(fechas))

        elif op == "8":
            reset_system()
            print("Sistema reiniciado.")

        elif op == "9":
            cargar_datos()

        elif op == "0":
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
