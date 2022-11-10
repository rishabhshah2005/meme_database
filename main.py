import mysql.connector as sql

con = sql.connect(host='localhost', user='root', passwd='root', database='memes')
cur = con.cursor()

def highest(cond):
    cur.execute("select * from memes_posted where upvotes = (select max(upvotes) from memes_posted)")
    ups = list(cur.fetchall()[0])
    cur.execute("select * from memes_posted where comments = (select max(comments) from memes_posted)")
    coms = list(cur.fetchall()[0])
    cur.execute("select * from memes_posted where awards = (select max(awards) from memes_posted)")
    awas = list(cur.fetchall()[0])

    if cond=='a':
        return awas
    elif cond=='u':
        return ups
    elif cond=='c':
        return coms
    

def min(cond):
    cur.execute("select * from memes_posted where upvotes = (select min(upvotes) from memes_posted)")
    ups = list(cur.fetchall()[0])
    cur.execute("select * from memes_posted where comments = (select min(comments) from memes_posted)")
    coms = list(cur.fetchall()[0])
    cur.execute("select * from memes_posted where awards = (select min(awards) from memes_posted)")
    awas = list(cur.fetchall()[0])

    if cond=='a':
        return awas
    elif cond=='u':
        return ups
    elif cond=='c':
        return coms
    
def average(field):
    cur.execute('select distinct template from memes_posted')
    temps = cur.fetchall()
    ans = []
    max=0
    greatest= ''
    for i in temps:
        cur.execute(f"select avg(t.{field}) from (select * from memes_posted where template='{i[0]}')t")
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
    max=0
    greatest= ''
    for i in temps:
        cur.execute(f"select count(template) from (select * from memes_posted where template='{i[0]}')t")
        data = cur.fetchall()
        ans.append(f"{i[0]} has been used {data[0][0]} times")
        if data[0][0]>max:
            max=data[0][0]
            greatest = i[0]
    ans.append(f"{greatest} is used the most")

    return ans

def search_id(id):
    cur.execute(f"select * from memes_posted where id={id}")
    result = cur.fetchall()
    return list(result[0])

if __name__ == '__main__':
    con = sql.connect(host='localhost', user='root', passwd='root', database='memes')
    cur = con.cursor()
    print(most_used())