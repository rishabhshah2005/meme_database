import mysql.connector as sql

con = sql.connect(host='localhost', user='root', passwd='root', database='memes')
cur = con.cursor()

def highest():
    cur.execute("select * from memes_posted where upvotes = (select max(upvotes) from memes_posted)")
    ups = cur.fetchall()
    cur.execute("select * from memes_posted where comments = (select max(comments) from memes_posted)")
    coms = cur.fetchall()
    cur.execute("select * from memes_posted where awards = (select max(awards) from memes_posted)")
    awas = cur.fetchall()
    print(ups)
    print(coms)
    print(awas[0])

def min():
    cur.execute("select * from memes_posted where upvotes = (select min(upvotes) from memes_posted)")
    ups = cur.fetchall()
    cur.execute("select * from memes_posted where comments = (select min(comments) from memes_posted)")
    coms = cur.fetchall()
    cur.execute("select * from memes_posted where awards = (select min(awards) from memes_posted)")
    awas = cur.fetchall()
    print(ups)
    print(coms)
    print(awas[0])

def average(field):
    cur.execute('select distinct template from memes_posted')
    temps = cur.fetchall()
    max=0
    greatest= ''
    for i in temps:
        cur.execute(f"select avg(t.{field}) from (select * from memes_posted where template='{i[0]}')t")
        avg = cur.fetchall()
        if avg[0][0] > max:
            max = avg[0][0]
            greatest = i[0]
        print(f"{i[0]} = {avg[0][0]}")

    print(greatest, 'is the most upvoted')

def most_used():
    cur.execute('select distinct template from memes_posted')
    temps = cur.fetchall()
    max=0
    greatest= ''
    for i in temps:
        cur.execute(f"select count(template) from (select * from memes_posted where template='{i[0]}')t")
        data = cur.fetchall()
        print(f"{i} has been used {data[0][0]}")
        if data[0][0]>max:
            max=data[0][0]
            greatest = i[0]
    print(f"{greatest} is used the most")

def search_id(id):
    cur.execute(f"select * from memes_posted where id={id}")
    result = cur.fetchall()
    for i in result:
        print(i)

