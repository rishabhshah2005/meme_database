import mysql.connector as sql
import random

con = sql.connect(host='localhost', user='root', passwd='root', database='memes')
cur = con.cursor()

templates=['coffin guys', 'drake', "undertaker behind aj styles", 'we are not the same', 'limmy waking up', 'homelander stressed', 'Leo DiCap', 'dog smiling', 'chotii bachhi ho kya', 'soldier boy', 'helikopter', 'this is fine', 'disappointed cricket fan', 'crying shaq', 'shocked penguin', 'noted']
typ = ["GIF", 'Image']


for i in range(1, 1001):
    temp = random.choice(templates)
    meme_type=random.choice(typ)
    upvote = random.randint(0, 100000)
    comment = random.randint(0, 20000)
    awards = random.randint(0, 100)
    cur.execute(f'insert into memes_posted values({i}, "{temp}", "{meme_type}", {upvote}, {comment}, {awards})')
    print(f"Record entered {i}")

con.commit()
print('DONE')
