import tkinter as tk
from tkinter import messagebox, filedialog
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
        
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        img = img.resize((200, 200), Image.LANCZOS)
        
        # Clear the center area for icon placement
        icon_size = 50
        center_x = (img.size[0] - icon_size) // 2
        center_y = (img.size[1] - icon_size) // 2
        for x in range(center_x, center_x + icon_size):
            for y in range(center_y, center_y + icon_size):
                img.putpixel((x, y), (255, 255, 255))  # Make center white for icon
        
        # Add icon image if selected
        if icon_path.get():
            try:
                icon = Image.open(icon_path.get())
                icon = icon.resize((icon_size, icon_size), Image.LANCZOS)  # Resize icon to fit in the center
                img.paste(icon, (center_x, center_y), icon)
            except Exception as e:
                messagebox.showerror("Icon Error", f"Failed to load icon: {e}")

        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk  # Keep a reference
    else:
        messagebox.showwarning("Input Error", "Please enter some data to generate QR code.")

def select_icon():
    file_path = filedialog.askopenfilename(
        title="Select Icon",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.ico")]
    )
    icon_path.set(file_path)

app = tk.Tk()
app.title("QR Code Generator with Icon")
app.geometry("400x500")

# Entry for text to encode
entry_label = tk.Label(app, text="Enter text or URL:")
entry_label.pack(pady=10)
entry = tk.Entry(app, width=40)
entry.pack(pady=10)

# Icon selection
icon_path = tk.StringVar()
select_icon_btn = tk.Button(app, text="Select Icon", command=select_icon)
select_icon_btn.pack(pady=5)

# Generate button
generate_btn = tk.Button(app, text="Generate QR Code", command=generate_qr)
generate_btn.pack(pady=20)

# Label for showing QR code
qr_label = tk.Label(app)
qr_label.pack(pady=10)

app.mainloop()
