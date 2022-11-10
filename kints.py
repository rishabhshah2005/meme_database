from tkinter import *
import mysql.connector as sql

cols = ['ID', "Template", 'Type', 'Upvotes', 'Comments', 'Awards']

#CONNECTING TO SQL
con = sql.connect(host='localhost', user='root',
                  passwd='root', database='memes')
cur = con.cursor()

#CREATING MAIN WINDOW
root = Tk()

##############################################################################################################


def highest(cond):
    cur.execute(
        "select * from memes_posted where upvotes = (select max(upvotes) from memes_posted)")
    ups = list(cur.fetchall()[0])
    cur.execute(
        "select * from memes_posted where comments = (select max(comments) from memes_posted)")
    coms = list(cur.fetchall()[0])
    cur.execute(
        "select * from memes_posted where awards = (select max(awards) from memes_posted)")
    awas = list(cur.fetchall()[0])

    if cond == 'a':
        return awas
    elif cond == 'u':
        return ups
    elif cond == 'c':
        return coms


def min(cond):
    cur.execute(
        "select * from memes_posted where upvotes = (select min(upvotes) from memes_posted)")
    ups = list(cur.fetchall()[0])
    cur.execute(
        "select * from memes_posted where comments = (select min(comments) from memes_posted)")
    coms = list(cur.fetchall()[0])
    cur.execute(
        "select * from memes_posted where awards = (select min(awards) from memes_posted)")
    awas = list(cur.fetchall()[0])

    if cond == 'a':
        return awas
    elif cond == 'u':
        return ups
    elif cond == 'c':
        return coms


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


def most_used():
    cur.execute('select distinct template from memes_posted')
    temps = cur.fetchall()
    ans = []
    max = 0
    greatest = ''
    for i in temps:
        cur.execute(
            f"select count(template) from (select * from memes_posted where template='{i[0]}')t")
        data = cur.fetchall()
        ans.append(f"{i[0]} has been used {data[0][0]} times")
        if data[0][0] > max:
            max = data[0][0]
            greatest = i[0]
    ans.append(f"{greatest} is used the most")

    return ans
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
        data = search_id(id)
        for i in cols:
            Label(frm, text=f'{i} = {data[cols.index(i)]}', font=('none', 12)).grid(
                column=0, rows=cols.index(i)+1, sticky='wn')

    clear_frame(win)
    frm = Frame(win)
    frm.grid(row=2, column=0, columnspan=3)
    Button(win, text="Home", padx=20, pady=15, font=('none', 20, 'bold'),
           command=lambda: home(root)).grid(row=3, column=0, columnspan=3, pady=40)
    Label(win, text="Enter ID: ", font=('none', 20),
          padx=5).grid(row=0, column=0, pady=30)
    id_ = Entry(win, width=17, justify=RIGHT, borderwidth=5, font=('none', 20))
    id_.grid(row=0, column=1)
    sea = Button(win, justify=LEFT, font=('none', 15), text="SEARCH",
                 command=lambda: display(id_.get(), frm)).grid(row=0, column=2, padx=5)


# HIGHEST
def high(win):

    def display(frm, cond):
        clear_frame(frm)
        data = highest(cond)
        for i in cols:
            Label(frm, text=f'{i} = {data[cols.index(i)]}', font=('none', 12)).grid(
                column=0, rows=cols.index(i)+1, sticky='wn')

    clear_frame(win)
    frm = Frame(win)
    frm.grid(row=2, column=0, columnspan=3, pady=10)

    Label(root, text="Search highest in terms of....", font=(
        'none', 20, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)
    Button(root, text='Upvotes', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'u')).grid(row=1, column=0, padx=8)
    Button(root, text='Comments', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'c')).grid(row=1, column=1, padx=8)
    Button(root, text='Awards', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'a')).grid(row=1, column=2, padx=8)
    Button(win, text="Home", font=("none", 20, 'bold'),
           command=lambda: home(root)).grid(row=3, column=0, columnspan=3)

# LOWEST


def low(win):

    def display(frm, cond):
        clear_frame(frm)
        data = min(cond)
        for i in cols:
            Label(frm, text=f'{i} = {data[cols.index(i)]}', font=('none', 12)).grid(
                column=0, rows=cols.index(i)+1, sticky='wn')

    clear_frame(win)
    frm = Frame(win)
    frm.grid(row=2, column=0, columnspan=3, pady=10)

    Label(root, text="Search lowest in terms of....", font=(
        'none', 20, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)
    Button(root, text='Upvotes', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'u')).grid(row=1, column=0, padx=8)
    Button(root, text='Comments', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'c')).grid(row=1, column=1, padx=8)
    Button(root, text='Awards', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'a')).grid(row=1, column=2, padx=8)
    Button(win, text="Home", font=("none", 20, 'bold'),
           command=lambda: home(root)).grid(row=3, column=0, columnspan=3)

# AVERAGE


def avg(win):
    def display(frm, cond):
        clear_frame(frm)
        data = average(cond)
        for i in data:
            Label(frm, text=i, font=('none', 12)).grid(
                column=0, rows=data.index(i)+1, sticky='wn')

    clear_frame(win)
    win.geometry('600x700')
    frm = Frame(win)
    frm.grid(row=2, column=0, columnspan=3, pady=10)

    Label(root, text="Search average of templates in...", font=(
        'none', 28, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)
    Button(root, text='Upvotes', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'upvotes')).grid(row=1, column=0, padx=8)
    Button(root, text='Comments', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'comments')).grid(row=1, column=1, padx=8)
    Button(root, text='Awards', padx=30, pady=20, font=('none', 19),
           command=lambda: display(frm, 'awards')).grid(row=1, column=2, padx=8)
    Button(win, text="Home", font=("none", 20, 'bold'),
           command=lambda: home(root)).grid(row=3, column=0, columnspan=3)


# OCCURANCES
def occurances(win):
    clear_frame(win)
    win.geometry('600x620')
    data = most_used()
    Label(win, text="No. of times a template has been used: ", padx=18, pady=8, font=(
        'none', 20, 'bold'), justify=CENTER).grid(row=1, column=0, columnspan=3, pady=10)
    frm = Frame(win)
    frm.grid(row=2, column=0, columnspan=3, pady=10)

    for i in data:
        Label(frm, text=i, font=('none', 12)).grid(
            column=0, rows=data.index(i)+1, sticky='wn')

    Button(win, text="Home", font=('none', 20, 'bold'), padx=5, pady=5,
           command=lambda: home(win)).grid(row=3, column=0, columnspan=3, pady=15)

# Home function


def home(root):
    root.geometry("600x510")
    clear_frame(root)
    intro = Label(root, text="Meme Database Management", padx=20, pady=20, font=(
        'none', 30, 'bold')).grid(row=0, column=0, columnspan=2)
    top_memes = Button(root, text='Top memes', padx=20, pady='20', font=(
        'none', 15, 'bold'), command=lambda: high(root)).grid(row=1, column=0, pady=20)
    low_memes = Button(root, text='Bottom memes', padx=20, pady='20', font=(
        'none', 15, 'bold'), command=lambda: low(root)).grid(row=1, column=1, pady=20)
    average = Button(root, text='Average', padx=20, pady='20', font=(
        'none', 15, 'bold'), command=lambda: avg(root)).grid(row=2, column=0, pady=20)
    most_used = Button(root, text='Most Used', padx=20, pady='20', font=(
        'none', 15, 'bold'), command=lambda: occurances(root)).grid(row=2, column=1, pady=20)
    search = Button(root, text='Search by ID', padx=60, pady='20', font=(
        'none', 15, 'bold'), command=lambda: search_(root)).grid(row=3, column=0, columnspan=2, pady=20)
    Label(root, text="Made by Rishabh Shah XII-A", pady=15, font=('none',
          15, 'bold')).grid(row=4, column=0, columnspan=2, pady=10)


home(root)

root.mainloop()
