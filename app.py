import PySimpleGUI as sg
import sqlite3

# Fungsi untuk membuat tabel jika belum ada
def create_table():
    connection = sqlite3.connect('mahasiswa.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mahasiswa (
                    id INTEGER PRIMARY KEY,
                    nama TEXT NOT NULL,
                    nim TEXT NOT NULL,
                    jurusan TEXT NOT NULL)''')
    connection.commit()
    connection.close()

# Fungsi untuk menambahkan data mahasiswa
def tambah_data(nilai, window):
    nama = nilai['nama']
    nim = nilai['nim']
    jurusan = nilai['jurusan']

    if nama and nim and jurusan:
        connection = sqlite3.connect('mahasiswa.db')
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO mahasiswa (nama, nim, jurusan)
                        VALUES (?, ?, ?)''', (nama, nim, jurusan))
        connection.commit()
        connection.close()
        sg.popup("Sukses", "Data mahasiswa berhasil ditambahkan")
        window['nama'].update('')
        window['nim'].update('')
        window['jurusan'].update('')
        tampilkan_data(window)
    else:
        sg.popup("Peringatan", "Mohon isi semua kolom!")

# Fungsi untuk menampilkan data mahasiswa
def tampilkan_data(window):
    connection = sqlite3.connect('mahasiswa.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM mahasiswa''')
    rows = cursor.fetchall()
    connection.close()

    window['-TABLE-'].update(values=rows)

# Fungsi untuk menghapus data mahasiswa
def hapus_data(nilai, window):
    baris_terpilih = nilai['-TABLE-']
    if baris_terpilih:
        connection = sqlite3.connect('mahasiswa.db')
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM mahasiswa WHERE id=?''', (baris_terpilih[0],))
        connection.commit()
        connection.close()
        sg.popup("Sukses", "Data mahasiswa berhasil dihapus")
        tampilkan_data(window)
    else:
        sg.popup("Peringatan", "Pilih data yang akan dihapus!")

# Membuat tata letak GUI
tata_letak = [
    [sg.Text('Nama:'), sg.InputText(key='nama')],
    [sg.Text('NIM:'), sg.InputText(key='nim')],
    [sg.Text('Jurusan:'), sg.InputText(key='jurusan')],
    [sg.Button('Tambah'), sg.Button('Hapus')],
    [sg.Table(values=[], headings=('ID', 'Nama', 'NIM', 'Jurusan'), key='-TABLE-')]
]

jendela = sg.Window('Aplikasi Data Mahasiswa', tata_letak)

create_table()  # Membuat tabel jika belum ada

while True:
    event, nilai = jendela.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == 'Tambah':
        tambah_data(nilai, jendela)
    elif event == 'Hapus':
        hapus_data(nilai, jendela)

jendela.close()
