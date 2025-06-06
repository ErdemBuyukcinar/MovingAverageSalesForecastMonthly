import tkinter as tk
from tkinter import messagebox, ttk

def ortalama_hesapla(veriler, periyot_sayisi):
    if len(veriler) < periyot_sayisi:
        raise ValueError(f"Yeterli veri yok. Ortalama için en az {periyot_sayisi} aylık veri gerekli.")
    
    ortalama = sum(veriler) / periyot_sayisi
    return ortalama

def hesapla_tahmin(periyot_sayisi_ortalama):
    try:
        ay_numarasi_tahmin = int(tahmin_ayi_entry.get())
        
        ay_sayisi_ortalama = periyot_sayisi_ortalama

        if ay_numarasi_tahmin <= ay_sayisi_ortalama:
            messagebox.showerror("Hata", 
                                 f"Tahmin edilecek ay ({ay_numarasi_tahmin}) için yeterli geçmiş veri yok.\n"
                                 f"'{ay_sayisi_ortalama} Aylık' ortalama için en az {ay_sayisi_ortalama + 1}. ayı tahmin etmelisiniz.")
            return

        start_index = ay_numarasi_tahmin - ay_sayisi_ortalama - 1 
        end_index = ay_numarasi_tahmin - 1

        if start_index < 0 or end_index > len(entries): 
             messagebox.showerror("Hata", 
                                 f"Hesaplama için gerekli geçmiş ay aralığı mevcut değil. "
                                 f"Lütfen '{ay_numarasi_tahmin}. Ay' tahminini destekleyecek kadar giriş alanı doldurduğunuzdan emin olun. "
                                 f"Mevcut veri giriş alanı sayısı: {len(entries)}")
             return

        relevant_sales_data = []
        for i in range(start_index, end_index):
            try:
                if i < len(entries): 
                    relevant_sales_data.append(float(entries[i].get()))
                else:
                    messagebox.showerror("Hata", "Hesaplama için gerekli tüm geçmiş satış verileri mevcut değil.")
                    return
            except ValueError:
                messagebox.showerror("Hata", "Lütfen tahmin için gerekli tüm geçmiş satış verilerini doldurun (sayısal olmalı).")
                return

        tahmin_ortalama = ortalama_hesapla(relevant_sales_data, ay_sayisi_ortalama)
        
        tahmin_label.config(text=f"{ay_numarasi_tahmin}. Ayın Satış Tahmini ({periyot_sayisi_ortalama} Aylık Ortalama): {tahmin_ortalama:.2f}")

        gelecek_veri = float(gelecek_veri_entry.get())
        
        tahmin_hatasi = abs(gelecek_veri - tahmin_ortalama)
        hata_label.config(text=f"{ay_numarasi_tahmin}. Ayın Tahmin Hatası: {tahmin_hatasi:.2f}")

        yuzde_hata = (tahmin_hatasi / gelecek_veri) * 100 if gelecek_veri != 0 else 0
        yuzde_label.config(text=f"Hata Yüzdesi: %{yuzde_hata:.2f}")
        
    except ValueError:
        messagebox.showerror("Hata", "Lütfen 'Tahmin Edilen Ay' ve 'Gerçekleşen Satış' alanlarına geçerli bir sayı girin.")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmeyen bir hata oluştu: {e}")

root = tk.Tk()
root.title("Aylık Satış Tahmini")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1) 

entries = []
for i in range(6): 
    ttk.Label(frame, text=f"{i+1}. Ay Satışı:").grid(row=i, column=0, padx=10, pady=3, sticky=tk.W)
    entry = ttk.Entry(frame, width=15)
    entry.grid(row=i, column=1, padx=10, pady=3, sticky=(tk.W, tk.E))
    entries.append(entry)

entries[0].insert(0, "1150") 
entries[1].insert(0, "1067") 
entries[2].insert(0, "183") 
entries[3].insert(0, "950")
entries[4].insert(0, "1100")
entries[5].insert(0, "1000")

ttk.Label(frame, text="Tahmin Edilen Ay:").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
tahmin_ayi_entry = ttk.Entry(frame, width=15)
tahmin_ayi_entry.grid(row=6, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))
tahmin_ayi_entry.insert(0, "7") 

gelecek_veri_label = ttk.Label(frame, text="Gerçekleşen Satış (Tahmin Edilen Ay İçin):")
gelecek_veri_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
gelecek_veri_entry = ttk.Entry(frame, width=15)
gelecek_veri_entry.grid(row=7, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))
gelecek_veri_entry.insert(0, "1050") 

hesapla_button_3aylik = ttk.Button(frame, text="3 AYLIK ORTALAMA İLE TAHMİNİ HESAPLA", command=lambda: hesapla_tahmin(3))
hesapla_button_3aylik.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

hesapla_button_6aylik = ttk.Button(frame, text="6 AYLIK ORTALAMA İLE TAHMİNİ HESAPLA", command=lambda: hesapla_tahmin(6))
hesapla_button_6aylik.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

tahmin_label = ttk.Label(frame, text="", font=("Helvetica", 12, "bold"))
tahmin_label.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

hata_label = ttk.Label(frame, text="", font=("Helvetica", 12, "bold"))
hata_label.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

yuzde_label = ttk.Label(frame, text="", font=("Helvetica", 12, "bold"))
yuzde_label.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
