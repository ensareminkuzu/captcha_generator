import qrcode
from PIL import Image
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

# Renk eşlemesi
color_mapping = {
    "siyah": "black",
    "mavi": "blue",
    "kırmızı": "red",
    "yeşil": "green",
    "sarı": "yellow",
    "mor": "purple",
    "beyaz": "white",
    "gri": "gray",
    "açık mavi": "lightblue",
    "pembe": "pink",
    "turuncu": "orange"
}








# QR kodu oluşturma fonksiyonu
def create_qr_code(url, resolution, qr_color, bg_color, save_path):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=min(resolution) // 29,
            border=4
        )
        qr.add_data(url)
        qr.make(fit=True)

        fill_color = color_mapping.get(qr_color, "black")
        back_color = color_mapping.get(bg_color, "white")

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img = img.convert("RGB")
        img.save(f"{save_path}.png")
        messagebox.showinfo("Başarılı", f"QR kodu başarıyla oluşturuldu: {save_path}.png")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# Dosya kaydetme konumu seçme fonksiyonu
def browse_location():
    save_path = filedialog.askdirectory()
    if save_path:
        save_path_entry.delete(0, tk.END)
        save_path_entry.insert(0, save_path)

# QR kodu oluşturma işlemini başlatma fonksiyonu
def generate_qr():
    url = url_entry.get()
    resolution = resolution_options[resolution_var.get()]
    qr_color = qr_color_var.get()
    bg_color = bg_color_var.get()
    save_path = save_path_entry.get() + "/" + file_name_entry.get()

    if url and save_path and file_name_entry.get():
        create_qr_code(url, resolution, qr_color, bg_color, save_path)
    else:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun ve bir dosya konumu seçin.")

# Tkinter arayüzü
root = tk.Tk()
root.title("QR Kod Oluşturucu")
root.geometry("500x375")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Başlık etiketi
title_label = tk.Label(root, text="QR Kod Oluşturucu", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#093c71")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Yuvarlatılmış köşeler için frame
frame = ttk.Frame(root, padding="10")
frame.grid(row=1, column=0, columnspan=2)

# URL Giriş alanı
tk.Label(frame, text="URL:", bg="#f0f0f0", fg="#000").grid(row=0, column=0, padx=10, pady=5, sticky="w")
url_entry = tk.Entry(frame, width=30, borderwidth=2)
url_entry.grid(row=0, column=1, padx=10, pady=5)

# Çözünürlük seçenekleri
resolution_options = {
    "Çok Küçük (50x50 px)": (50, 50),
    "Küçük (100x100 px)": (100, 100),
    "Orta (200x200 px)": (200, 200),
    "Büyük (300x300 px)": (300, 300),
    "Çok Büyük (500x500 px)": (500, 500)
}
tk.Label(frame, text="Çözünürlük:", bg="#f0f0f0", fg="#000").grid(row=1, column=0, padx=10, pady=5, sticky="w")
resolution_var = tk.StringVar(value="Orta (200x200 px)")
resolution_menu = ttk.Combobox(frame, textvariable=resolution_var, values=list(resolution_options.keys()), state="readonly")
resolution_menu.grid(row=1, column=1, padx=10, pady=5)

# Renk kutusu fonksiyonu
def color_menu(parent, var, options):
    menu = ttk.Combobox(parent, textvariable=var, values=options, state="readonly")
    menu.bind('<<ComboboxSelected>>', lambda event: menu.config(background=color_mapping[var.get()]))
    return menu

# QR Kodu Rengi seçenekleri
qr_colors = list(color_mapping.keys())
tk.Label(frame, text="QR Kodu Rengi:", bg="#f0f0f0", fg="#000").grid(row=2, column=0, padx=10, pady=5, sticky="w")
qr_color_var = tk.StringVar(value="siyah")
qr_color_menu = color_menu(frame, qr_color_var, qr_colors)
qr_color_menu.grid(row=2, column=1, padx=10, pady=5)

# Arka Plan Rengi seçenekleri
bg_colors = list(color_mapping.keys())
tk.Label(frame, text="Arka Plan Rengi:", bg="#f0f0f0", fg="#000").grid(row=3, column=0, padx=10, pady=5, sticky="w")
bg_color_var = tk.StringVar(value="beyaz")
bg_color_menu = color_menu(frame, bg_color_var, bg_colors)
bg_color_menu.grid(row=3, column=1, padx=10, pady=5)

# Dosya adı giriş alanı
tk.Label(frame, text="Dosya Adı:", bg="#f0f0f0", fg="#000").grid(row=4, column=0, padx=10, pady=5, sticky="w")
file_name_entry = tk.Entry(frame, width=20, borderwidth=2)
file_name_entry.grid(row=4, column=1, padx=10, pady=5)

# Kaydetme konumu seçici
tk.Label(frame, text="Kaydetme Konumu:", bg="#f0f0f0", fg="#000").grid(row=5, column=0, padx=10, pady=5, sticky="w")
save_path_entry = tk.Entry(frame, width=20, borderwidth=2)
save_path_entry.grid(row=5, column=1, padx=10, pady=5)

# Gözat butonu
browse_button = tk.Button(frame, text="Gözat", command=browse_location, bg="#093c71", fg="white", width=15, height=1)  # width değeri artırıldı
browse_button.grid(row=5, column=2, padx=5, pady=0)  # Gözat butonunun solundaki boşlukları artırabilirsiniz

# Oluştur butonu
generate_button = tk.Button(root, text="QR Kodu Oluştur", command=generate_qr, bg="#093c71", fg="white", height=2, width=20)
generate_button.grid(row=6, column=0, columnspan=2, pady=20)

root.mainloop()
