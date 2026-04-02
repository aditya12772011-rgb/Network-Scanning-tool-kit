import socket
import subprocess
import threading
from queue import Queue

# --- CONFIGURATION ---
# Replace this with your actual local subnet (e.g., 192.168.1.)
DEFAULT_SUBNET = "192.168.1." 
THREADS = 100

def get_my_ip():
    """Tool 5: Find your own local IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def ping_host(ip):
    """Tool 4: Ping Scanning"""
    # -c 1 (send 1 packet), -W 1 (wait 1 second)
    command = ["ping", "-c", "1", "-W", "1", ip]
    return subprocess.run(command, stdout=subprocess.DEVNULL).returncode == 0

def scan_port(ip, port):
    """Tool 1 & 3: Port/Force Scanning"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                return True
    except:
        pass
    return False

def network_scanner(subnet):
    """Tool 1 & 5: Find connected devices and their IPs"""
    print(f"\n[!] Scanning subnet {subnet}0/24...")
    active_devices = []
    
    def worker(q):
        while not q.empty():
            ip = q.get()
            if ping_host(ip):
                print(f"[+] Device Found: {ip}")
                active_devices.append(ip)
            q.task_done()

    q = Queue()
    for i in range(1, 255):
        q.put(subnet + str(i))

    for _ in range(THREADS):
        t = threading.Thread(target=worker, args=(q,))
        t.daemon = True
        t.start()
    
    q.join()
    return active_devices

def main_menu():
    while True:
        print("\n--- PYTHON NETWORK TOOLSET (NON-ROOT) ---")
        print("1. Network Scanning (Scan Subnet)")
        print("2. Network Management (Host Info)")
        print("3. Force Port Scanning (Scan specific IP)")
        print("4. Ping Scanning (Check specific IP)")
        print("5. Find My IP & Device Info")
        print("0. Exit")
        
        choice = input("\nSelect an option: ")

        if choice == '1' or choice == '5':
            # Finds connected devices and lists their IPs
            my_ip = get_my_ip()
            print(f"Your IP: {my_ip}")
            subnet = ".".join(my_ip.split(".")[:-1]) + "."
            network_scanner(subnet)

        elif choice == '2':
            # Management: Get Hostname and Status
            target = input("Enter IP to manage: ")
            try:
                name = socket.gethostbyaddr(target)[0]
                print(f"Device Name: {name}")
            except:
                print("Could not resolve hostname.")
            print(f"Status: {'Online' if ping_host(target) else 'Offline'}")

        elif choice == '3':
            # Force Scanning: Check a range of ports on one device
            target = input("Enter Target IP: ")
            print(f"Force scanning common ports on {target}...")
            for port in [21, 22, 80, 443, 3306, 5555, 8080]:
                if scan_port(target, port):
                    print(f"[OPEN] Port {port}")

        elif choice == '4':
            # Ping Scanning
            target = input("Enter IP to Ping: ")
            if ping_host(target):
                print(f"{target} is UP.")
            else:
                print(f"{target} is DOWN/UNREACHABLE.")

        elif choice == '0':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
  
