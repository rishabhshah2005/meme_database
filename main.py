from tkinter import *
import mysql.connector as sql


cols = ['ID', "Template", 'Type', 'Upvotes', 'Comments', 'Awards']

# CONNECTING TO SQL
con = sql.connect(host='localhost', user='root',
                  passwd='root', database='memes')
cur = con.cursor()

# CREATING MAIN WINDOW
root = Tk()
root.configure(bg='#a2b9fc')


##############################################################################################################


def delete_by_id(id):
    cur.execute(f'delete from memes_posted where id={id}')
    con.commit()


def insert_stuff(id, temp, typ, ups, comms, awds):
    cur.execute(
        f"insert into memes_posted values({id}, '{temp}', '{typ}', {ups}, {comms}, {awds})")
    con.commit()


def average(field):
    cur.execute('select distinct template from memes_posted')
    temps = cur.fetchall()
    ans = []
    max = 0
    greatest = ''
    for i in temps:
        cur.execute(
            f"select avg(t.{field}) from (select * from memes_posted where template='{i[0]}')t")
        avg = cur.fetchall()
        if avg[0][0] > max:
            max = avg[0][0]
            greatest = i[0]
        ans.append(f"{i[0]} = {avg[0][0]}")

    ans.append(greatest + ' is the most upvoted')
    return ans


def change(id, temp, typ, ups, comms, awds):
    cur.execute(
        f"update memes_posted set template='{temp}', type='{typ}', upvotes={ups}, comments={comms}, awards={awds} where id={id}")
    con.commit()


###############################################################################################################################

# SEARCH


def search_id(id):
    cur.execute(f"select * from memes_posted where id={id}")
    result = cur.fetchall()
    return list(result[0])

# CLEAR FRAME


def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


# SEARCH BY ID


def search_(win):
    def display(id, frm):
        clear_frame(frm)
        try:
            data = search_id(id)
            for i in cols:
                Label(frm, text=f'{i} = {data[cols.index(i)]}', font=('none', 12), bg='#a2b9fc').grid(
                    column=0, rows=cols.index(i)+1, sticky='wn')
        
        except IndexError:
            Label(frm, text='ID not found', font=('none', 18, 'bold'), bg='#a2b9fc').pack()

    clear_frame(win)
    frm = Frame(win)
    frm.grid(row=2, column=0, columnspan=3)
    frm.configure(bg='#a2b9fc')
    Button(win, text="Home", padx=20, pady=15, font=('none', 20, 'bold'),
           command=lambda: home(root), bg='#fafa90').grid(row=3, column=0, columnspan=3, pady=40)
    Label(win, text="Enter ID: ", font=('none', 20),
          padx=20, bg='#a2b9fc').grid(row=0, column=0, pady=30)
    id_ = Entry(win, width=17, justify=RIGHT, borderwidth=5, font=('none', 20))
    id_.grid(row=0, column=1)
    sea = Button(win, justify=LEFT, font=('none', 15), text="SEARCH",
                 command=lambda: display(id_.get(), frm), bg='#fafa90').grid(row=0, column=2, padx=5)


def delete(win):
    def display(id, frm):
        clear_frame(frm)
        try:
            delete_by_id(id)

            Label(frm, text='Done', font=('none', 14, 'bold'),
                  padx=5, pady=5, bg='#a2b9fc').pack()

        except:
            Label(frm, text='ERROR', font=('none', 14, 'bold'),
                  padx=5, pady=5, bg='#a2b9fc').pack()

    clear_frame(win)
    frm = Frame(win)
    frm.grid(row=2, column=0, columnspan=3)
    frm.configure(bg='#a2b9fc')
    Button(win, text="Home", padx=20, pady=15, font=('none', 20, 'bold'),
           command=lambda: home(root), bg='#fafa90').grid(row=3, column=0, columnspan=3, pady=40)
    Label(win, text="Enter ID: ", font=('none', 20),
          padx=5, bg='#a2b9fc').grid(row=0, column=0, pady=30)
    id_ = Entry(win, width=17, justify=RIGHT, borderwidth=5, font=('none', 20))
    id_.grid(row=0, column=1)
    sea = Button(win, justify=LEFT, font=('none', 15), text="Delete",
                 command=lambda: display(id_.get(), frm), bg='#fafa90').grid(row=0, column=2, padx=5)


def update(win):
    def display(frm, id, temp, typ, ups, comms, awds):
        clear_frame(frm)
        try:
            change(id, temp, typ, ups, comms, awds)
            Label(frm, text=f"ID-{id} UPDATED", font=('none',
                19, 'bold'), padx=7, pady=7, bg='#a2b9fc').pack()
        
        except:
            Label(frm, text=f"ERROR", font=('none',
                19, 'bold'), padx=7, pady=7, bg='#a2b9fc').pack()            

    clear_frame(win)
    frm = Frame(win)
    frm.grid(row=7, column=0, columnspan=3)
    Label(win, text="ID", padx=8, pady=5, font=('none', 15, 'bold'),
          bg='#a2b9fc').grid(row=0, column=0, pady=10)
    Label(win, text="Template", padx=8, pady=5, font=(
        'none', 15, 'bold'), bg='#a2b9fc').grid(row=1, column=0, pady=10)
    Label(win, text="Type", padx=8, pady=5, font=('none', 15, 'bold'),
          bg='#a2b9fc').grid(row=2, column=0, pady=10)
    Label(win, text="Upvotes", padx=8, pady=5, font=('none', 15, 'bold'),
          bg='#a2b9fc').grid(row=3, column=0, pady=10)
    Label(win, text="Comments", padx=8, pady=5, font=(
        'none', 15, 'bold'), bg='#a2b9fc').grid(row=4, column=0, pady=10)
    Label(win, text="Awards", padx=8, pady=5, font=('none', 15, 'bold'),
          bg='#a2b9fc').grid(row=5, column=0, pady=10)

    id_ = Entry(win, width=17, justify=RIGHT, borderwidth=5, font=('none', 20))
    id_.grid(column=1, row=0, pady=10)
    temp_ = Entry(win, width=17, justify=RIGHT,
                  borderwidth=5, font=('none', 20))
    temp_.grid(column=1, row=1, pady=10)
    typ_ = Entry(win, width=17, justify=RIGHT,
                 borderwidth=5, font=('none', 20))
    typ_.grid(column=1, row=2, pady=10)
    ups_ = Entry(win, width=17, justify=RIGHT,
                 borderwidth=5, font=('none', 20))
    ups_.grid(column=1, row=3, pady=10)
    comms_ = Entry(win, width=17, justify=RIGHT,
                   borderwidth=5, font=('none', 20))
    comms_.grid(column=1, row=4, pady=10)
    awds_ = Entry(win, width=17, justify=RIGHT,
                  borderwidth=5, font=('none', 20))
    awds_.grid(column=1, row=5, pady=10)

    Button(win, text="Update", font=('none', 20, 'bold'), padx=7, pady=10, command=lambda: display(frm, id_.get(), temp_.get(
    ), typ_.get(), ups_.get(), comms_.get(), awds_.get()), bg='#fafa90').grid(row=0, column=2, rowspan=3, padx=40)
    Button(win, text="HOME", font=('none', 20, 'bold'), padx=7, pady=10, command=lambda: home(
        root), bg='#fafa90').grid(row=3, column=2, rowspan=3, padx=40)


def insert(win):
    def display(frm, id, temp, typ, ups, comms, awds):
        clear_frame(frm)
        try:
            insert_stuff(id, temp, typ, ups, comms, awds)
            Label(frm, text=f"ID-{id} INSERTED", font=('none',
                  19, 'bold'), padx=7, pady=7, bg='#a2b9fc').pack()
        except:
            Label(frm, text="ERROR", font=('none', 19, 'bold'),
                  padx=7, pady=7, bg='#a2b9fc').pack()

    clear_frame(win)
    frm = Frame(win)
    frm.grid(row=7, column=0, columnspan=3)
    Label(win, text="ID", padx=8, pady=5, font=('none', 15, 'bold'),
          bg='#a2b9fc').grid(row=0, column=0, pady=10)
    Label(win, text="Template", padx=8, pady=5, font=(
        'none', 15, 'bold'), bg='#a2b9fc').grid(row=1, column=0, pady=10)
    Label(win, text="Type", padx=8, pady=5, font=('none', 15, 'bold'),
          bg='#a2b9fc').grid(row=2, column=0, pady=10)
    Label(win, text="Upvotes", padx=8, pady=5, font=('none', 15, 'bold'),
          bg='#a2b9fc').grid(row=3, column=0, pady=10)
    Label(win, text="Comments", padx=8, pady=5, font=(
        'none', 15, 'bold'), bg='#a2b9fc').grid(row=4, column=0, pady=10)
    Label(win, text="Awards", padx=8, pady=5, font=('none', 15, 'bold'),
          bg='#a2b9fc').grid(row=5, column=0, pady=10)

    id_ = Entry(win, width=17, justify=RIGHT, borderwidth=5, font=('none', 20))
    id_.grid(column=1, row=0, pady=10)
    temp_ = Entry(win, width=17, justify=RIGHT,
                  borderwidth=5, font=('none', 20))
    temp_.grid(column=1, row=1, pady=10)
    typ_ = Entry(win, width=17, justify=RIGHT,
                 borderwidth=5, font=('none', 20))
    typ_.grid(column=1, row=2, pady=10)
    ups_ = Entry(win, width=17, justify=RIGHT,
                 borderwidth=5, font=('none', 20))
    ups_.grid(column=1, row=3, pady=10)
    comms_ = Entry(win, width=17, justify=RIGHT,
                   borderwidth=5, font=('none', 20))
    comms_.grid(column=1, row=4, pady=10)
    awds_ = Entry(win, width=17, justify=RIGHT,
                  borderwidth=5, font=('none', 20))
    awds_.grid(column=1, row=5, pady=10)

    Button(win, text="Insert", font=('none', 20, 'bold'), padx=7, pady=10, command=lambda: display(frm, id_.get(), temp_.get(
    ), typ_.get(), ups_.get(), comms_.get(), awds_.get()), bg='#fafa90').grid(row=0, column=2, rowspan=3, padx=40)
    Button(win, text="HOME", font=('none', 20, 'bold'), padx=7, pady=10, command=lambda: home(
        root), bg='#fafa90').grid(row=3, column=2, rowspan=3, padx=40)


def avg(win):
    def display(frm, cond):
        clear_frame(frm)
        data = average(cond)
        for i in data:
            Label(frm, text=i, font=('none', 12), bg='#a2b9fc').grid(
                column=0, rows=data.index(i)+1, sticky='wn')

    clear_frame(win)
    win.geometry('600x700')
    frm = Frame(win)
    frm.grid(row=2, column=0, columnspan=3, pady=10)
    frm.configure(bg='#a2b9fc')

    Label(root, text="Search average of templates in...", font=(
        'none', 28, 'bold'), bg='#a2b9fc').grid(row=0, column=0, columnspan=3, pady=10)
    Button(root, text='Upvotes', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'upvotes'), bg='#fafa90').grid(row=1, column=0, padx=8)
    Button(root, text='Comments', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'comments'), bg='#fafa90').grid(row=1, column=1, padx=8)
    Button(root, text='Awards', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'awards'), bg='#fafa90').grid(row=1, column=2, padx=8)
    Button(win, text="Home", font=("none", 20, 'bold'),
           command=lambda: home(root), bg='#fafa90').grid(row=3, column=0, columnspan=3)

# Home function


def home(root):
    root.geometry("595x530")
    clear_frame(root)

    intro = Label(root, text="Meme Database Management", padx=20, pady=20, font=(
        'none', 30, 'bold'), bg='#a2b9fc').grid(row=0, column=0, columnspan=2)
  # #fafa65
    delete_ = Button(root, text='Delete by ID', padx=20, pady='20', font=(
        'none', 15, 'bold'), command=lambda: delete(root), bg='#fafa90').grid(row=1, column=0, pady=20)
    update_meme = Button(root, text='Update Data', padx=20, pady='20', font=(
        'none', 15, 'bold'), command=lambda: update(root), bg='#fafa90').grid(row=1, column=1, pady=20)
    average = Button(root, text='Average', padx=20, pady='20', font=(
        'none', 15, 'bold'), command=lambda: avg(root), bg='#fafa90').grid(row=2, column=0, pady=20)
    insert_ = Button(root, text='Insert Data', padx=20, pady='20', font=(
        'none', 15, 'bold'), command=lambda: insert(root), bg='#fafa90').grid(row=2, column=1, pady=20)
    search = Button(root, text='Search by ID', padx=60, pady='20', font=(
        'none', 15, 'bold'), command=lambda: search_(root), bg='#fafa90').grid(row=3, column=0, columnspan=2, pady=20)
    Label(root, text="Made by Rishabh Shah XII-A", pady=15, font=('none',
          15, 'bold'), bg='#a2b9fc').grid(row=4, column=0, columnspan=2, pady=10)


home(root)

root.mainloop()
