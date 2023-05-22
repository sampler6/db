import pyodbc
import tkinter as tk
root = tk.Tk()
root.title("Артисты")
conn = pyodbc.connect(driver='{SQL Server}',
               server='127.0.0.1',
               database='db22204',
               user='User027',
               password='User027*]71')
cursor = conn.cursor()


def load_tbl_artist():
    # Заполнение имени
    cursor.execute("Select txtArtistSurname, txtArtistName from tblArtist")
    tmp = cursor.fetchall()
    for i in range(0, len(tmp)):
        name = tmp[i]
        str_i = str(i + 1) + ") " + name[0].replace(" ", "") + " " + name[1].replace(" ", "")
        tbl_artist_table[0].insert(i, str_i)
    # Заполнение псевдонима
    cursor.execute("Select txtArtistStageName from tblArtist")
    tmp = cursor.fetchall()
    num = len(tmp)
    for i in range(0, num):
        name = tmp[i]
        str_i = str(i + 1) + ") " + " ".join(name[0].split())
        tbl_artist_table[1].insert(i, str_i)
    # Заполнение названия коллектива, города и стиля
    cursor.execute("Select intArtistGroupid from tblArtist")
    tmp = cursor.fetchall()
    group_id = dict()
    for i in range(0, num):
        group_id[i] = int(str(tmp[i][0]))
    for i in range(0, num):
        cursor.execute("Select txtGroupName, txtGroupCity, txtGroupStyle from tblArtistGroup where intArtistGroupId="
                       + str(group_id[i]))
        tmp = cursor.fetchone()
        for j in range(3):
            tbl_artist_table[2 + j].insert(i, str(i + 1) + ") " + " ".join(tmp[j].split()))


def tbl_artist():
    root.geometry("1200x700")
    root.minsize(1200, 400)
    lbl_artist.pack(pady=1)
    #Расположение форм + подписей
    frm_tbl_artist_main.pack(fill=tk.BOTH, expand=True, padx=30, pady=60)
    for i in range(5):
        frm_tbl_artist[i].place(relx=0.03 + i*0.1975, rely=0.05, relwidth=0.15, relheight=0.9)
        lbl_tbl_artist[i].pack()
    #Расположение листбоксов
    for table in tbl_artist_table:
        table.pack(fill=tk.BOTH, expand=True)


#tbl_artist
frm_artist = tk.Frame(master=root, height=10, width=10, bg="#24908A")
frm_artist.pack(fill=tk.BOTH, expand=True)

lbl_artist = tk.Label(master=frm_artist, text="Артисты", font=("Roboto", 20, "bold"), bg="#24908A", fg="white")
frm_tbl_artist_main = tk.Frame(master=frm_artist, bg="#D9D9D9")

#Внутренние формы + подписи к ним
frm_tbl_artist = list()
lbl_tbl_artist = list()
for title in ["Фамилия и имя", "Псевдоним", "Название коллектива", "Город", "Стиль"]:
    frm_tbl_artist.append(tk.Frame(master=frm_tbl_artist_main, bg="#B49F9F", bd=2, relief=tk.SOLID))
    lbl_tbl_artist.append(tk.Label(master=frm_tbl_artist[len(frm_tbl_artist)-1], text=title, font=("Roboto", 9, "bold"),
                                   bg="#DBCCCC", bd=2, relief=tk.SOLID, width=600, height=2))

#листбоксы для форм
tbl_artist_scroll = tk.Scrollbar(master=frm_tbl_artist_main)
tbl_artist_table = list()
for i in range(5):
    tbl_artist_table.append(tk.Listbox(master=frm_tbl_artist[i], bg="#B49F9F", fg="white",
                                       yscrollcommand=tbl_artist_scroll.set, font=("Roboto", 10, "bold")))

tbl_artist()
load_tbl_artist()

root.mainloop()
