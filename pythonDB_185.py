import sqlite3  # Modul untuk mengelola database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Modul untuk membuat GUI

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database SQLite
    cursor = conn.cursor()  # Membuat kursor untuk eksekusi SQL
    # Membuat tabel `nilai_siswa` jika belum ada
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nama_siswa TEXT,  
            biologi INTEGER,  
            fisika INTEGER,  
            inggris INTEGER, 
            prediksi_fakultas TEXT 
        )
    ''')
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk mengambil semua data dari tabel `nilai_siswa`
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data
    rows = cursor.fetchall()  # Mengambil hasil query sebagai list
    conn.close()  # Menutup koneksi
    return rows  # Mengembalikan data

# Fungsi untuk menyimpan data baru ke tabel `nilai_siswa`
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    # Menyisipkan data baru
    cursor.execute('''  
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk memperbarui data dalam tabel `nilai_siswa`
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    # Memperbarui data berdasarkan ID
    cursor.execute('''  
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghapus data berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # Prediksi berdasarkan nilai Biologi
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # Prediksi berdasarkan nilai Fisika
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # Prediksi berdasarkan nilai Inggris
    else:
        return "Tidak diketahui"  # Jika tidak ada nilai dominan

# Fungsi untuk menyimpan data baru saat tombol submit ditekan
def submit():
    try:
        # Mengambil data dari input
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:  # Validasi nama tidak boleh kosong
            raise Exception("Nama siswa tidak boleh kosong.")
        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data ke database

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Mengosongkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:  # Menangani error input
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data saat tombol update ditekan
def update():
    try:
        if not selected_record_id.get():  # Validasi jika tidak ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk diupdate!")
        
        # Mengambil data dari input
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:  # Validasi nama tidak boleh kosong
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Memperbarui data di database

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", "Data berhasil diperbarui")
        clear_inputs()  # Mengosongkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:  # Menangani error input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data saat tombol delete ditekan
def delete():
    try:
        if not selected_record_id.get():  # Validasi jika tidak ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")
        
        record_id = int(selected_record_id.get())  # Mengambil ID data yang akan dihapus
        delete_database(record_id)  # Menghapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()  # Mengosongkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:  # Menangani error input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan semua input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():  # Menghapus semua data lama di tabel
        tree.delete(row)
    for row in fetch_data():  # Menambahkan data baru dari database
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi input berdasarkan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mengambil baris yang dipilih
        selected_row = tree.item(selected_item)['values']  # Mendapatkan data dari baris

        selected_record_id.set(selected_row[0])  # Mengisi ID data yang dipilih
        nama_var.set(selected_row[1])  # Mengisi nama siswa
        biologi_var.set(selected_row[2])  # Mengisi nilai Biologi
        fisika_var.set(selected_row[3])  # Mengisi nilai Fisika
        inggris_var.set(selected_row[4])  # Mengisi nilai Inggris
    except IndexError:  # Jika tidak ada data yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database dan membuat tabel jika belum ada
create_database()

# Membuat GUI menggunakan Tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")
root.configure(bg="lightblue")  # Mengatur warna latar belakang jendela

# Variabel untuk input data
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Variabel untuk menyimpan ID data yang dipilih

# Membuat label dan input untuk nama dan nilai siswa
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol untuk tambah, update, dan hapus data dengan warna
Button(root, text="Add", command=submit, bg="lightgreen", fg="black").grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update, bg="pink", fg="black").grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete, bg="salmon", fg="black").grid(row=4, column=2, pady=10)

# Membuat tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Menyesuaikan posisi teks di setiap kolom ke tengah
for col in columns:
    tree.heading(col, text=col.capitalize())  # Menentukan judul kolom
    tree.column(col, anchor='center')  # Menentukan posisi teks

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Menempatkan tabel di GUI

# Event untuk memilih data dari tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Mengisi tabel dengan data dari database
populate_table()

# Menjalankan aplikasi GUI
root.mainloop()
