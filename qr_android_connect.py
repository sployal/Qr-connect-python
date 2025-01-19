import qrcode
import socket
from PIL import Image, ImageTk
import tkinter as tk
import threading

# Function to generate QR code
def generate_qr():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    port = 12345
    ip_port = f"{local_ip}:{port}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(ip_port)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    img.save('ip_qr.png')
    
    return 'ip_qr.png', ip_port

# Function to check connection status
def check_connection(ip_port):
    ip, port = ip_port.split(":")
    port = int(port)
    
    try:
        sock = socket.create_connection((ip, port), timeout=5)
        return f"Connected to {ip}:{port}"
    except socket.error:
        return f"Connection to {ip}:{port} failed"

# Function to start server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), 12345))
    server_socket.listen(5)
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            print(f"Received: {msg.decode('utf-8')}")
        
        client_socket.close()

# Function to show QR code
def show_qr():
    img_path, ip_port = generate_qr()

    def update_status():
        status_label.config(text="Connecting...")
        status = check_connection(ip_port)
        status_label.config(text=status)
    
    root = tk.Tk()
    root.title("QR Code")
    
    img = Image.open(img_path)
    img = ImageTk.PhotoImage(img)
    
    qr_label = tk.Label(root, image=img)
    qr_label.pack()
    
    status_label = tk.Label(root, text="Idle", font=("Helvetica", 12))
    status_label.pack(pady=10)
    
    connect_button = tk.Button(root, text="Check Connection", command=lambda: threading.Thread(target=update_status).start())
    connect_button.pack(pady=5)
    
    threading.Thread(target=start_server).start()
    
    root.mainloop()

show_qr()
