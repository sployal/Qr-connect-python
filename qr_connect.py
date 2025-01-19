import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk

def generate_qr():
    data = entry.get()
    if data:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((200, 200), Image.LANCZOS)  # Changed ANTIALIAS to LANCZOS
        
        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk  # Keep a reference
    else:
        messagebox.showwarning("Input Error", "Please enter some data to generate QR code.")

app = tk.Tk()
app.title("QR Code Generator")
app.geometry("400x400")

# Entry for text to encode
entry_label = tk.Label(app, text="Enter text or URL:")
entry_label.pack(pady=10)
entry = tk.Entry(app, width=40)
entry.pack(pady=10)

# Generate button
generate_btn = tk.Button(app, text="Generate QR Code", command=generate_qr)
generate_btn.pack(pady=20)

# Label for showing QR code
qr_label = tk.Label(app)
qr_label.pack(pady=10)

app.mainloop()
