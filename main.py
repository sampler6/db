import tkinter

import pyodbc
import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("Артисты")
conn = pyodbc.connect(driver='{SQL Server}',
                      server='127.0.0.1',
                      database='db22204',
                      user='User027',
                      password='User027*]71')
cursor = conn.cursor()


def load_tbl_artist(table):
    for i in table.get_children():
        table.delete(i)
    # Заполнение имени
    cursor.execute("Select intArtistId, txtArtistSurname, txtArtistName from tblArtist")
    tmp = cursor.fetchall()
    artists_rows = list()
    for i in range(len(tmp)):
        artists_rows.append(list())
    for i in range(0, len(tmp)):
        name = tmp[i]
        artists_rows[i].append(str(name[0]))
        str_i = name[1].replace(" ", "") + " " + name[2].replace(" ", "")
        artists_rows[i].append(str_i)
    # Заполнение псевдонима
    cursor.execute("Select txtArtistStageName from tblArtist")
    tmp = cursor.fetchall()
    num = len(tmp)
    for i in range(0, num):
        name = tmp[i]
        str_i = " ".join(name[0].split())
        artists_rows[i].append(str_i)
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
            artists_rows[i].append(" ".join(tmp[j].split()))
    for row in artists_rows:
        table.insert('', tk.END, values=row)


def load_tbl_concert(table, selected_row):
    for i in table.get_children():
        table.delete(i)

    concert_rows = list()
    cursor.execute("Select intConcertId, fltParticipateSum from tblParticipate where intArtistId=" + selected_row[0])
    tmp = cursor.fetchall()
    for i in range(len(tmp)):
        concert_rows.append(list())
        cursor.execute("Select txtTitle, datConcertDate, intHallId from tblConcert where intConcertId=" +
                       str(tmp[i][0]))
        tmp1 = cursor.fetchone()
        concert_rows[i].append(" ".join(tmp1[0].split()))
        concert_rows[i].append(tmp1[1])
        hall = tmp1[2]
        cursor.execute("Select txtHallName, txtHallAddress from tblHall where intHallId=" + str(hall))
        tmp2 = cursor.fetchone()
        concert_rows[i].append(" ".join(tmp2[0].split()))
        concert_rows[i].append(" ".join(tmp2[1].split()))
        concert_rows[i].append(tmp[i][1])

    for row in concert_rows:
        table.insert('', tk.END, values=row)


def tbl_artist(table):
    lbl_artist.place(rely=0, relx=0.5, relheight=0.1)
    frm_tbl_artist_main.place(rely=0.1, relx=0, relheight=0.8, relwidth=1)
    btn_add_artist.place(rely=0.9, relx=0.9, relwidth=0.1, relheight=0.1)
    headers = ["id", "Фамилия и имя", "Псевдоним", "Название коллектива", "Город", "Стиль"]
    table['columns'] = headers
    for header in headers:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center')
    load_tbl_artist(table)
    table.pack(expand=tkinter.YES, fill=tk.BOTH)


def push_tbl_artist(entry, cmbbox, group_dict):
    name, surname = entry[0].get().split(maxsplit=2)
    nickname = entry[1].get()
    id = group_dict[cmbbox.get()]
    income = entry[2].get()
    cursor.execute("insert into tblArtist Values (\'" + name + "\', \'" +
                   surname + "\', \'" + nickname + "\', " + str(id) + ", " + str(income) + ")")
    #cursor.commit()
    load_tbl_artist(table_tbl_artist)


def add_artist():
    window_add_artist = tk.Toplevel(root, bg="#24908A")
    window_add_artist.geometry("1300x150")
    window_add_artist.minsize(1000, 100)
    window_add_artist.title("Добавить артиста")
    headers = ["Имя Фамилия", "Псевдоним", "Название коллектива", "Доход"]
    for i in range(4):
        tk.Label(window_add_artist, text=headers[i]).place(relx=0.25 * i, relwidth=0.25, rely=0.2, relheight=0.2)
    entry = list()
    for i in range(2):
        entry.append(tk.Entry(window_add_artist))
        entry[i].place(relx=0.25 * i, relwidth=0.25, rely=0.4, relheight=0.2)
    entry.append(tk.Entry(window_add_artist))
    entry[2].place(relx=0.25 * 3, relwidth=0.25, rely=0.4, relheight=0.2)
    cursor.execute("Select intArtistGroupId, txtGroupName from tblArtistGroup")
    tmp = cursor.fetchall()
    group_list = list()
    group_dict = dict()
    for i in range(len(tmp)):
        group_id = tmp[i][0]
        group_name = " ".join(tmp[i][1].split())
        group_dict[group_name] = group_id
        group_list.append(group_name)
    cmbbox_add_artist = ttk.Combobox(window_add_artist, values=group_list, state="readonly")
    cmbbox_add_artist.place(relx=0.25 * 2, relwidth=0.25, rely=0.4, relheight=0.2)

    btn_add = tk.Button(window_add_artist, text="Добавить", command=lambda: push_tbl_artist(entry, cmbbox_add_artist, group_dict))
    btn_close = tk.Button(window_add_artist, text="Отмена",
                        command=lambda: window_add_artist.destroy())
    btn_add.place(relx=0.90, rely=0.8, relwidth=0.1)
    btn_close.place(relx=0.80, rely=0.8, relwidth=0.1)


def tbl_concert_init():
    lbl_concert.place(rely=0, relx=0.5, relheight=0.1)
    headers = ["Название концерта", "Дата", "Название зала", "Адрес", "Гонорар артиста"]
    table_tbl_concert['columns'] = headers
    for header in headers:
        table_tbl_concert.heading(header, text=header, anchor='center')
        table_tbl_concert.column(header, anchor='center')
    table_tbl_concert.place(rely=0.2, relx=0, relheight=0.7, relwidth=0.95)
    table_tbl_concert_scrollbar.place(rely=0.2, relx=0.95, relwidth=0.05, relheight=0.7)
    btn_add_concert.place(rely=0.9, relx=0.9, relwidth=0.1, relheight=0.1)
    btn_close_concert.place(rely=0.9, relx=0.8, relwidth=0.1, relheight=0.1)


def tbl_concert(self):
    table = table_tbl_artist
    selected_row = table.item(table.focus(), 'values')
    frm_artist.pack_forget()

    frm_concert.pack(expand=tkinter.YES, fill=tk.BOTH)
    table = ttk.Treeview(frm_concert, show='headings')
    headers = ["id", "Фамилия и имя", "Псевдоним", "Название коллектива", "Город", "Стиль"]
    btn_add_concert.configure(command=lambda: add_concert(selected_row))
    table['columns'] = headers
    for header in headers:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center')
    table.place(rely=0.1, relwidth=1, height=47)
    table.insert('', tk.END, values=selected_row)
    btn_close_concert.config(command=lambda: close_concert(table))
    load_tbl_concert(table_tbl_concert, selected_row)


def add_concert(selected_row):
    window_add_concert = tk.Toplevel(root, bg="#24908A")
    window_add_concert.geometry("1300x150")
    window_add_concert.minsize(1000, 100)
    window_add_concert.maxsize(1500, 300)
    window_add_concert.title("Добавить артиста")
    headers = ["Название концерта", "Название композиции", "Порядковый номер", "Гонорар"]
    for i in range(4):
        tk.Label(window_add_concert, text=headers[i]).place(relx=0.25 * i, relwidth=0.25, rely=0.2, relheight=0.2)
    entry = list()
    entry.append(tk.Entry(window_add_concert))
    entry.append(tk.Entry(window_add_concert))
    entry.append(tk.Entry(window_add_concert))
    entry[0].place(relx=0.25 * 1, relwidth=0.25, rely=0.4, relheight=0.2)
    entry[1].place(relx=0.25 * 2, relwidth=0.25, rely=0.4, relheight=0.2)
    entry[2].place(relx=0.25 * 3, relwidth=0.25, rely=0.4, relheight=0.2)
    cursor.execute("Select intConcertId, txtTitle from tblConcert")
    tmp = cursor.fetchall()
    concert_list = list()
    concert_dict = dict()
    for i in range(len(tmp)):
        concert_id = tmp[i][0]
        concert_name = " ".join(tmp[i][1].split())
        concert_dict[concert_name] = concert_id
        concert_list.append(concert_name)
    cmbbox_add_concert = ttk.Combobox(window_add_concert, values=concert_list, state="readonly")
    cmbbox_add_concert.place(relx=0.25 * 0, relwidth=0.25, rely=0.4, relheight=0.2)

    btn_add = tk.Button(window_add_concert, text="Добавить",
                        command=lambda: push_tbl_concert(entry, cmbbox_add_concert, concert_dict, selected_row))
    btn_close = tk.Button(window_add_concert, text="Отмена",
                          command=lambda: window_add_concert.destroy())
    btn_add.place(relx=0.90, rely=0.8, relwidth=0.1)
    btn_close.place(relx=0.80, rely=0.8, relwidth=0.1)


def push_tbl_concert(entry, cmbbox_add_concert, concert_dict, selected_row):
    composition = entry[0].get()
    number = entry[1].get()
    sum = entry[2].get()
    cursor.execute("insert into tblParticipate Values (\'" + str(selected_row[0]) + "\', \'" +
                   str(concert_dict[cmbbox_add_concert.get()]) + "\', " + str(sum) + ", \'" +
                   composition + "\', " + str(number) + ")")
    # cursor.commit()
    load_tbl_concert(table_tbl_concert, selected_row)


def close_concert(table):
    frm_concert.pack_forget()
    table.place_forget()
    frm_artist.pack(expand=tkinter.YES, fill=tk.BOTH)


root.geometry("1200x700")
root.minsize(1200, 400)
frm_artist = tk.Frame(master=root, bg="#24908A")
frm_artist.pack(expand=tkinter.YES, fill=tk.BOTH)

frm_concert = tk.Frame(master=root, bg="#24908A")
lbl_concert = tk.Label(master=frm_concert, text="Концерты", font=("Roboto", 20, "bold"), bg="#24908A", fg="white")
table_tbl_concert = ttk.Treeview(frm_concert, show='headings')
table_tbl_concert_scrollbar = ttk.Scrollbar(frm_concert, command=table_tbl_concert.yview)
table_tbl_concert.configure(yscrollcommand=table_tbl_concert_scrollbar)
btn_add_concert = tk.Button(frm_concert, text="Добавить концерт")
btn_close_concert = tk.Button(frm_concert, text="Назад", command=close_concert)

lbl_artist = tk.Label(master=frm_artist, text="Артисты", font=("Roboto", 20, "bold"), bg="#24908A", fg="white")
frm_tbl_artist_main = tk.Frame(master=frm_artist, bg="#D9D9D9")
table_tbl_artist = ttk.Treeview(frm_tbl_artist_main, show='headings')
table_tbl_artist_scrollbar = ttk.Scrollbar(frm_tbl_artist_main, command=table_tbl_artist.yview)
table_tbl_artist.configure(yscrollcommand=table_tbl_artist_scrollbar)
table_tbl_artist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
btn_add_artist = tk.Button(frm_artist, text="Добавить артиста", command=add_artist)
table_tbl_artist.bind("<Double-1>", tbl_concert)


tbl_artist(table_tbl_artist)
tbl_concert_init()

root.mainloop()
