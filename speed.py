import tkinter as tk
import speedtest
import threading
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
from PIL import Image, ImageTk
import requests

# Bağlantı durumu etiketini güncelleme
def update_connection_status(status):
    connection_status_label.config(text=f"Bağlantı Durumu: {status}")

# Hız testi fonksiyonu
def run_speed_test():
    try:
        # Bağlantı durumu güncelle
        update_connection_status("Bağlantı Test Ediliyor...")

        # Progress bar'ı başlat
        progress_bar.start()

        # SpeedTest nesnesi oluşturuluyor
        st = speedtest.Speedtest()
        st.get_best_server()  # En iyi sunucuyu seçiyor

        # Ping, download ve upload hızlarını alıyoruz
        ping = st.results.ping
        download_speed = st.download() / 1_000_000  # Mbps cinsinden
        upload_speed = st.upload() / 1_000_000  # Mbps cinsinden

        # Sonuçları GUI'ye yazdırıyoruz
        ping_label.config(text=f"Ping: {ping} ms")
        download_label.config(text=f"İndirme Hızı: {download_speed:.2f} Mbps")
        upload_label.config(text=f"Yükleme Hızı: {upload_speed:.2f} Mbps")

        # Bağlantı durumu güncelle
        update_connection_status("Bağlantı Başarılı!")

        # Progress bar'ı durdur
        progress_bar.stop()

        # Grafik verilerini hazırlıyoruz
        data = [ping, download_speed, upload_speed]
        labels = ['Ping (ms)', 'İndirme (Mbps)', 'Yükleme (Mbps)']
        
        # Grafik çizimi
        ax.clear()
        ax.bar(labels, data, color=['red', 'blue', 'green'])
        ax.set_ylabel('Hız / Ping')
        ax.set_title('Hız Testi Sonuçları')

        # Grafik gösterimi
        canvas.draw()

        # Grafik widget'ını görünür yapıyoruz
        canvas.get_tk_widget().pack(pady=20)
        
        # Form boyutunu grafiğe göre güncelleme
        root.geometry("600x650")

    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
        progress_bar.stop()  # Hata durumunda progress bar'ı durdur

        # Grafik widget'ını gizli tut
        canvas.get_tk_widget().pack_forget()

# ALG Yazılım linkine tıklanması için fonksiyon
def open_website(event=None):
    webbrowser.open("https://algyazilim.com")

# Hakkında formunu oluştur
def open_about():
    about_window = tk.Toplevel(root)
    about_window.title("Hakkında")
    about_window.geometry("600x350")
    about_window.config(bg="#f0f0f0")
    about_window.resizable(False, False)

    # Hakkında formunu merkeze yerleştir
    about_window.geometry("+{}+{}".format(int(root.winfo_width()/2 - 300), int(root.winfo_height()/2 - 175)))

    # Canvas ekle
    canvas = tk.Canvas(about_window, bg="#f0f0f0", width=380, height=220)
    canvas.pack(pady=20)

    # Hakkında metni için bir Label oluştur
    about_text = "ALG Yazılım, yazılım geliştirme alanında uzmanlaşmış bir teknoloji şirketidir. \n" \
                 "Müşterilerine yenilikçi çözümler sunmayı hedefler. \n\n" \
                 "İnternet hız testi, yazılım geliştirme ve çeşitli dijital hizmetler sunar."

    about_label = tk.Label(canvas, text=about_text, font=("Helvetica", 12), bg="#f0f0f0", fg="#2c3e50", justify="left")
    about_label.pack(padx=10, pady=10)

    # Logo Resmi
    logo_url = "https://yazilim.algyazilim.com/wp-content/uploads/2023/09/ALG-Yazilim-.png"
    response = requests.get(logo_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((150, 150), Image.Resampling.LANCZOS)  # Logoyu uygun boyutlandır
    logo = ImageTk.PhotoImage(img)

    # Logo'yu formda yerleştirme
    logo_label = tk.Label(about_window, image=logo, bg="#f0f0f0")
    logo_label.image = logo  # Referans tutmak için ekleme
    logo_label.pack(pady=10)

    # ALG Yazılım Inc.© - 2024 yazısı ekleniyor
    footer_label = tk.Label(about_window, text="ALG Yazılım Inc.© - 2024", font=("Helvetica", 10), fg="#2980b9", bg="#f0f0f0")
    footer_label.pack(pady=5)

    # Logo ve yazıya tıklanabilirlik ekliyoruz
    logo_label.bind("<Button-1>", open_website)
    footer_label.bind("<Button-1>", open_website)

# Ana pencereyi oluştur
root = tk.Tk()
root.title("INT TestSpeed App | ALG Yazılım Inc.© 2024")
root.geometry("600x600")
root.config(bg="#2c3e50")  # Arka plan rengini koyu yapıyoruz
root.resizable(False, False)  # Formu sabitle

# Ana formu merkeze yerleştir
root.geometry("+{}+{}".format(int(root.winfo_screenwidth()/2 - 300), int(root.winfo_screenheight()/2 - 300)))

# Menü barı oluştur
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Bağlantı durumu etiketi
connection_status_label = tk.Label(root, text="Bağlantı Durumu: Bağlantı Bekleniyor...", font=("Helvetica", 12), fg="white", bg="#2c3e50")
connection_status_label.pack()

# Ping, download ve upload etiketlerini oluştur
ping_label = tk.Label(root, text="Ping: 0 ms", font=("Helvetica", 14), fg="white", bg="#2c3e50")
ping_label.pack(pady=5)

download_label = tk.Label(root, text="İndirme Hızı: 0 Mbps", font=("Helvetica", 14), fg="white", bg="#2c3e50")
download_label.pack(pady=5)

upload_label = tk.Label(root, text="Yükleme Hızı: 0 Mbps", font=("Helvetica", 14), fg="white", bg="#2c3e50")
upload_label.pack(pady=5)

# Test başlatma butonu
start_button = tk.Button(root, text="Test Başlat", font=("Helvetica", 12), bg="#8eba00", fg="white", command=lambda: threading.Thread(target=run_speed_test).start())
start_button.pack(pady=20)

# Progress bar'ı ekle
progress_bar = ttk.Progressbar(root, length=200, mode="indeterminate")
progress_bar.pack(pady=20)

# Grafik alanını oluştur
fig, ax = plt.subplots(figsize=(6, 3))
canvas = FigureCanvasTkAgg(fig, master=root)

# Hakkında butonunu ekle
about_button = tk.Button(root, text="Hakkında", font=("Helvetica", 12), bg="#8eba00", fg="white", command=open_about)
about_button.pack(pady=10)

# Uygulamayı başlat
root.mainloop()
