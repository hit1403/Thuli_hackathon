import socket
import subprocess
import platform

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return None

def get_all_ips():
    """Get all network interfaces and their IPs"""
    system = platform.system()
    ips = []
    
    try:
        if system == "Windows":
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'IPv4 Address' in line:
                    ip = line.split(':')[-1].strip()
                    if ip and not ip.startswith('127.'):
                        ips.append(ip)
        else:
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            # Parse ifconfig output for IPs
            lines = result.stdout.split('\n')
            for line in lines:
                if 'inet ' in line and '127.0.0.1' not in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'inet' and i + 1 < len(parts):
                            ip = parts[i + 1]
                            if '.' in ip and not ip.startswith('127.'):
                                ips.append(ip)
    except Exception as e:
        print(f"Error getting network interfaces: {e}")
    
    return ips

def main():
    print("Finding your computer's IP addresses for React Native...")
    print("=" * 50)
    
    # Get primary local IP
    local_ip = get_local_ip()
    if local_ip:
        print(f"Primary IP Address: {local_ip}")
        print(f"   Use this for physical devices: http://{local_ip}:8000")
    
    # Get all network IPs
    all_ips = get_all_ips()
    if all_ips:
        print(f"\nAll Network Interfaces:")
        for ip in all_ips:
            print(f"   - {ip}")
    
    print(f"\nReact Native Configuration:")
    print(f"   Android Emulator: http://10.0.2.2:8000")
    print(f"   iOS Simulator: http://localhost:8000")
    if local_ip:
        print(f"   Physical Device: http://{local_ip}:8000")
    
    print(f"\nTo update your app configuration:")
    print(f"   Edit: frontend/src/services/config.js")
    print(f"   Change PHYSICAL_DEVICE to: 'http://{local_ip}:8000'")
    
    print(f"\nTest your backend:")
    print(f"   Browser: http://localhost:8000")
    if local_ip:
        print(f"   Device: http://{local_ip}:8000")

if __name__ == "__main__":
    main()
