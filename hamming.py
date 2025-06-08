import tkinter as tk
from tkinter import ttk, messagebox


def hesapla_r(m):
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1
    return r
def kod_olustur(veri):
    m = len(veri)
    r = hesapla_r(m)
    toplam_uzunluk = m + r
    kod = ['_' for _ in range(toplam_uzunluk)]
    # Veriyi sağdan sola yerleştirme
    veri_rev = veri[::-1]
    j = 0
    for i in range(toplam_uzunluk):
        if (i + 1) & i == 0:
            continue
        if j < m:
            kod[i] = veri_rev[j]
            j += 1
        else:
            kod[i] = '0'
    # Eski check değerini hesapla (sadece veri bitlerinin 1 olduğu pozisyonların XOR'u)
    # Pozisyonlar 1-tabanlı ve LSB'den başlar (kod[0] = pos 1, kod[1] = pos 2, ...)
    eski_check = 0
    adimlar = []
    for i, bit_char in enumerate(kod):
        pos = i + 1
        if (pos & (pos - 1)) == 0:
            continue
        if bit_char == '1':
            eski_check ^= pos
            ikili = format(pos, '0{}b'.format(r))
            adimlar.append(f"{ikili} (pozisyon {pos})")
    # Parite bitlerini yerleştir
    for k_parity_index in range(r):
        parity_bit_pos_1_based = (2 ** k_parity_index)
        idx_in_kod_array = parity_bit_pos_1_based - 1
        bit_degeri_for_parity = (eski_check >> k_parity_index) & 1
        kod[idx_in_kod_array] = str(bit_degeri_for_parity)
    # DED için ek parite biti ekle (MSB pozisyonunda)
    total_ones = kod.count('1')
    kod.insert(0, '1' if total_ones % 2 == 1 else '0')  # Even parity için
    kod_str = ''.join(kod[::-1])
    eski_check_ikili = format(eski_check, '0{}b'.format(r))
    return kod, kod_str, r, eski_check, eski_check_ikili, adimlar


def yeni_check_hesapla(kod, r):
    yeni_check = 0
    adimlar = []
    # Pozisyonlar 1-tabanlı ve LSB'den başlar
    for i, bit_char in enumerate(kod):
        pos = i + 1
        if (pos & (pos - 1)) == 0:
            continue
        if bit_char == '1':
            yeni_check ^= pos
            ikili = format(pos, '0{}b'.format(r))
            adimlar.append(f"{ikili} (pozisyon {pos})")
    yeni_check_ikili = format(yeni_check, '0{}b'.format(r))
    return yeni_check, yeni_check_ikili, adimlar


def toggle_ded_input(*args):
    if mode_var.get() == "DED":
        lbl_hata2.grid()
        entry_hata2.grid()
        lbl_hata1.config(text="1. Hata eklenecek bit no:")
    else:
        lbl_hata2.grid_remove()
        entry_hata2.grid_remove()
        entry_hata2.delete(0, tk.END)
        lbl_hata1.config(text="Hata eklenecek bit no:")


def simule_et():
    veri_girdi = entry_veri.get().replace(" ", "")
    if not veri_girdi or not all(c in '01' for c in veri_girdi):
        messagebox.showerror("Hata", "Lütfen yalnızca 0 ve 1 kullanın.")
        return
    if len(veri_girdi) not in (8, 16, 32):
        messagebox.showerror("Hata", "Veri uzunluğu 8, 16 veya 32 bit olmalı.")
        return
    # --- Kod Oluşturma (Her iki mod için ortak) ---
    kod, kod_str, r, eski_check, eski_check_ikili, adimlar_eski = kod_olustur(veri_girdi)
    text_sonuc.delete("1.0", tk.END)
    text_sonuc.insert(tk.END, "Parity bitleri yerleştirilmeden önce veri bitlerinin 1 olduğu pozisyonlar:\n")
    for a in adimlar_eski:
        text_sonuc.insert(tk.END, f"- {a}\n")
    text_sonuc.insert(tk.END, f"\nCheck bitleri (XOR sonucu): {eski_check_ikili}\n")
    text_sonuc.insert(tk.END, "Parity bitleri (check bitleri) sırasıyla (p1, p2, p4, p8, ...):\n\n")
    text_sonuc.insert(tk.END, f"Hamming kodlu blok (toplam {len(kod)} bit): {kod_str}\n")
    text_sonuc.insert(tk.END, f"MSB parite biti (DED için): {kod[0]}\n\n")
    for k in range(r):
        idx = (2 ** k)
        text_sonuc.insert(tk.END, f"- p{2**k} (dizi indeksi {idx}, 1-başlayan pos {idx+1}): {kod[idx]}\n")
    # --- SEC Modu ---
    if mode_var.get() == "SEC":
        hata_pos_str = entry_hata.get().strip()
        if hata_pos_str:
            try:
                pos = int(hata_pos_str)
                idx_hata = pos - 1
                if idx_hata < 0 or idx_hata >= len(kod):
                    raise ValueError
                bozuk = kod.copy()
                bozuk[idx_hata] = '1' if bozuk[idx_hata] == '0' else '0'
                bozuk_str = ''.join(bozuk[::-1])
                text_sonuc.insert(tk.END, f"\nHata eklendi (pos {pos}): {bozuk_str}\n\n")
                yeni_check, yeni_check_ikili, adimlar_yeni = yeni_check_hesapla(bozuk, r)
                text_sonuc.insert(tk.END, "Hata eklenmiş blokta veri bitlerinin 1 olduğu pozisyonlar:\n")
                for a in adimlar_yeni:
                    text_sonuc.insert(tk.END, f"- {a}\n")
                text_sonuc.insert(tk.END, f"\nYeni check bitleri: {yeni_check_ikili}\n")
                syndrome = eski_check ^ yeni_check
                syndrome_ikili = format(syndrome, '0{}b'.format(r))
                text_sonuc.insert(tk.END, f"\nSyndrome hesaplama:\n")
                text_sonuc.insert(tk.END, f"Eski check:    {eski_check_ikili}\n")
                text_sonuc.insert(tk.END, f"Yeni check:    {yeni_check_ikili}\n")
                text_sonuc.insert(tk.END, f"XOR sonucu:    {syndrome_ikili}\n")
                if syndrome == 0:
                    text_sonuc.insert(tk.END, "⚠️ Orijinal veride hata yok.\n")
                else:
                    text_sonuc.insert(tk.END, f"❗ Hatalı bit pozisyonu: {syndrome}\n")
                    text_sonuc.insert(tk.END, f" Düzeltildi: {kod_str}\n")
            except ValueError:
                messagebox.showerror("Hata", "Geçersiz hata pozisyonu.")
        else:
            text_sonuc.insert(tk.END, "\nHata eklenmedi.\n")
    # --- DED Modu ---
    elif mode_var.get() == "DED":
        text_sonuc.insert(tk.END, "\n--- DED Modu Simülasyonu ---\n")
        hata_pos_str1 = entry_hata.get().strip()
        hata_pos_str2 = entry_hata2.get().strip()
        bozuk_ded = kod.copy()
        actual_errors_introduced = []
        if not hata_pos_str1 and not hata_pos_str2:
            text_sonuc.insert(tk.END, "DED Modu: Simülasyon için en az bir hata pozisyonu girilmelidir.\n")
            return
        # 1. Hata
        if hata_pos_str1:
            try:
                pos1 = int(hata_pos_str1)
                idx_hata1 = pos1 - 1
                if not (0 <= idx_hata1 < len(bozuk_ded)): raise ValueError("1. Hata pozisyonu aralık dışında.")
                original_bit1 = bozuk_ded[idx_hata1]
                bozuk_ded[idx_hata1] = '1' if bozuk_ded[idx_hata1] == '0' else '0'
                actual_errors_introduced.append(pos1)
                bozuk_ded_str_err1 = ''.join(bozuk_ded[::-1])
                text_sonuc.insert(tk.END, f"\n1. Hata {pos1}. pozisyonda eklendi (bit {original_bit1} -> {bozuk_ded[idx_hata1]}).\n")
                text_sonuc.insert(tk.END, f"Blok 1. hatadan sonra: {bozuk_ded_str_err1}\n")
            except ValueError as e:
                messagebox.showerror("Hata", f"Geçersiz 1. hata pozisyonu: {e}")
                return
        # 2. Hata
        if hata_pos_str2:
            try:
                pos2 = int(hata_pos_str2)
                idx_hata2 = pos2 - 1
                if not (0 <= idx_hata2 < len(bozuk_ded)): raise ValueError("2. Hata pozisyonu aralık dışında.")
                original_bit2 = bozuk_ded[idx_hata2]
                bozuk_ded[idx_hata2] = '1' if bozuk_ded[idx_hata2] == '0' else '0'
                if pos1 == pos2 and hata_pos_str1:  # Aynı yere ikinci hata
                    text_sonuc.insert(tk.END, f"\n2. hata tekrar {pos2}. pozisyonda eklendi (bit {original_bit2} -> {bozuk_ded[idx_hata2]}).\n")
                    text_sonuc.insert(tk.END, f"Bu, {pos1}. pozisyondaki bitin orijinal haline dönmesi anlamına gelir.\n")
                    actual_errors_introduced.remove(pos1)
                else:
                    actual_errors_introduced.append(pos2)
                    text_sonuc.insert(tk.END, f"\n2. hata {pos2}. pozisyonda eklendi (bit {original_bit2} -> {bozuk_ded[idx_hata2]}).\n")
                bozuk_ded_str_err2 = ''.join(bozuk_ded[::-1])
                text_sonuc.insert(tk.END, f"Blok 2. hatadan sonra: {bozuk_ded_str_err2}\n\n")
            except ValueError as e:
                messagebox.showerror("Hata", f"Geçersiz 2. hata pozisyonu: {e}")
                return
        yeni_check_ded, yeni_check_ded_ikili, adimlar_yeni_ded = yeni_check_hesapla(bozuk_ded, r)
        text_sonuc.insert(tk.END, "Sonraki blokta veri bitlerinin 1 olduğu pozisyonlar:\n")
        for a in adimlar_yeni_ded:
            text_sonuc.insert(tk.END, f"- {a}\n")
        text_sonuc.insert(tk.END, f"\nYeni check: {yeni_check_ded_ikili}\n")
        syndrome_ded = eski_check ^ yeni_check_ded
        syndrome_ded_ikili = format(syndrome_ded, '0{}b'.format(r))
        text_sonuc.insert(tk.END, f"\nSyndrome hesaplama (DED):\n")
        text_sonuc.insert(tk.END, f"Eski check:    {eski_check_ikili}\n")
        text_sonuc.insert(tk.END, f"Yeni check:    {yeni_check_ded_ikili}\n")
        text_sonuc.insert(tk.END, f"XOR sonucu:    {syndrome_ded_ikili}\n")
        # Hata düzeltme ve parite kontrolü
        duzeltilmis_kod = bozuk_ded.copy()
        if syndrome_ded != 0:
            # Sendrom sıfırdan farklı ise, hatalı biti düzeltmeyi dene
            hatali_bit_pos = syndrome_ded - 1  # 0-based index
            if 0 <= hatali_bit_pos < len(duzeltilmis_kod):
                # MSB'yi (en soldaki bit) değiştirme
                duzeltilmis_kod[hatali_bit_pos] = '1' if duzeltilmis_kod[hatali_bit_pos] == '0' else '0'
                text_sonuc.insert(tk.END, f"\nHata düzeltme denemesi:\n")
                text_sonuc.insert(tk.END, f"Düzeltilen bit pozisyonu: {hatali_bit_pos + 1}\n")
                text_sonuc.insert(tk.END, f"Düzeltilmiş kod: {''.join(duzeltilmis_kod[::-1])}\n")
        # Parite kontrolü ve düzeltme
        total_ones = duzeltilmis_kod.count('1')
        is_even_parity = total_ones % 2 == 0
        if not is_even_parity:
            # Parite tek ise, en soldaki biti (MSB) değiştir
            duzeltilmis_kod[-1] = '1' if duzeltilmis_kod[-1] == '0' else '0'  # En soldaki bit
            text_sonuc.insert(tk.END, f"\nParite düzeltme:\n")
            text_sonuc.insert(tk.END, f"En soldaki bit değiştirildi: {duzeltilmis_kod[-1]}\n")
            text_sonuc.insert(tk.END, f"Son düzeltilmiş kod: {''.join(duzeltilmis_kod[::-1])}\n")
        # Son durum analizi
        text_sonuc.insert(tk.END, f"\nDED Modu Son Durum Analizi:\n")
        text_sonuc.insert(tk.END, f"Toplam 1'lerin sayısı: {duzeltilmis_kod.count('1')}\n")
        text_sonuc.insert(tk.END, f"Parite durumu: {'Çift' if duzeltilmis_kod.count('1') % 2 == 0 else 'Tek'}\n")
        num_actual_errors = len(actual_errors_introduced)
        error_pos_list_str = ", ".join(map(str, sorted(list(set(actual_errors_introduced))))) if actual_errors_introduced else "yok"
        text_sonuc.insert(tk.END, f"Simülasyonda net {num_actual_errors} bit hatası eklendi (pozisyonlar: {error_pos_list_str}).\n")
        text_sonuc.insert(tk.END, f"Son düzeltilmiş kod: {''.join(duzeltilmis_kod[::-1])}\n")
        if num_actual_errors == 0:
            text_sonuc.insert(tk.END, "✓ Veri hatasız.\n")
        elif num_actual_errors == 1:
            if syndrome_ded != 0:
                text_sonuc.insert(tk.END, "✓ Tek hata başarıyla düzeltildi.\n")
            else:
                text_sonuc.insert(tk.END, "⚠️ Hata tespit edilemedi (parite biti hatası olabilir).\n")
        else:
            text_sonuc.insert(tk.END, "⚠️ Çift veya daha fazla hata var! Düzeltme güvenilir değil.\n")


# --- GUI Kurulumu ---
window = tk.Tk()
window.title("Hamming SEC / DED Simülatörü")
window.geometry("800x600")
# Mode selection
mode_var = tk.StringVar(value="SEC")
mode_frame = ttk.Frame(window, padding=(10, 0, 10, 5))
mode_frame.pack(fill="x")
ttk.Label(mode_frame, text="Mod Seçimi:").pack(side="left", padx=(0, 10))
sec_radio = ttk.Radiobutton(mode_frame, text="SEC (Tek Hata Düzeltme)", variable=mode_var, value="SEC", command=toggle_ded_input)
sec_radio.pack(side="left", padx=5)
ded_radio = ttk.Radiobutton(mode_frame, text="DED (Çift Hata Tespiti Sim.)", variable=mode_var, value="DED", command=toggle_ded_input)
ded_radio.pack(side="left", padx=5)
frame = ttk.Frame(window, padding=10)
frame.pack(fill="x")
ttk.Label(frame, text="Veri (8, 16 veya 32 bit):").grid(row=0, column=0, sticky="w", pady=2)
entry_veri = ttk.Entry(frame, width=50)
entry_veri.grid(row=0, column=1, columnspan=2, padx=10, pady=2, sticky="ew")
# Hata pozisyonu girişleri
lbl_hata1_text = "Hata eklenecek bit no:"
lbl_hata1 = ttk.Label(frame, text=lbl_hata1_text)
lbl_hata1.grid(row=1, column=0, sticky="w", pady=2)
entry_hata = ttk.Entry(frame, width=10)
entry_hata.grid(row=1, column=1, padx=10, pady=2, sticky="w")
lbl_hata2 = ttk.Label(frame, text="2. Hata eklenecek bit no:")
lbl_hata2.grid(row=2, column=0, sticky="w", pady=2)
entry_hata2 = ttk.Entry(frame, width=10)
entry_hata2.grid(row=2, column=1, padx=10, pady=2, sticky="w")
# Başlangıçta DED için olanı gizle
lbl_hata2.grid_remove()
entry_hata2.grid_remove()
btn = ttk.Button(frame, text="Simüle Et", command=simule_et)
btn.grid(row=3, column=0, columnspan=3, pady=10)
frame.columnconfigure(1, weight=1)
text_sonuc = tk.Text(window, height=25, wrap="word", font=("Courier New", 10))
text_sonuc.pack(padx=10, pady=10, fill="both", expand=True)
window.mainloop()


