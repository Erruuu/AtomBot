import MySQLdb
import MySQLdb.cursors

import time

import discord


class MySQL:
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "4rYk5vZMNQQqCxsW", "proton", cursorclass=MySQLdb.cursors.DictCursor)
        self.cur = self.db.cursor()

        self.db.autocommit(True)

    # CHECKS
    def userExists(self, user):
        self.cur.execute(f"SELECT * FROM users WHERE UID={user.id}")
        return len(self.cur.fetchall())

    def serverExists(self, server):
        self.cur.execute(f"SELECT * FROM servers WHERE SID={server.id}")
        return len(self.cur.fetchall())

    # FUNCTIONS
    def createUser(self, user):
        self.cur.execute(f"INSERT INTO users (UID) VALUES ({user.id})")

    def createServer(self, server):
        self.cur.execute(f"INSERT INTO servers (SID) VALUES ({server.id})")

    def userGet(self, user):
        self.cur.execute(f"SELECT * FROM users WHERE UID={user.id}")
        return self.cur.fetchone()

    def serverGet(self, server):
        self.cur.execute(f"SELECT * FROM servers WHERE SID={server.id}")
        return self.cur.fetchone()

    def serverSet(self, server, field, new):
        self.cur.execute(f"UPDATE servers SET {field}={new} WHERE SID={server.id}")

    # ECONOMY RELATED
    def updateDaily(self, user):
        self.cur.execute(f"UPDATE users SET LDaily={time.time()} WHERE UID={user.id}")

    def addMoney(self, user, amt):
        self.cur.execute(f"SELECT Money FROM users WHERE UID={user.id}")
        current = self.cur.fetchone()['Money']
        self.cur.execute(f"UPDATE users SET Money={current+amt} WHERE UID={user.id}")

    def delMoney(self, user, amt):
        self.cur.execute(f"SELECT Money FROM users WHERE UID={user.id}")
        current = self.cur.fetchone()['Money']
        self.cur.execute(f"UPDATE users SET Money={current-amt} WHERE UID={user.id}")

    # LEVEL RELATED
    async def addXP(self, message, amt, user=None):
        if user is None:
            user = message.author

        self.cur.execute(f"SELECT * FROM users WHERE UID={user.id}")
        row = self.cur.fetchone()
        cXP = row['XP']
        cLevel = row['Level']
        levelUp = False

        xpMult = 150

        nXP = cXP + amt
        nLevel = cLevel

        while nXP >= nLevel * xpMult:
            levelUp = True
            nXP -= nLevel * xpMult
            nLevel += 1

        self.cur.execute(f"UPDATE users SET XP={nXP}, Level={nLevel} WHERE UID={user.id}")

        if levelUp:
            await message.channel.send(embed=discord.Embed(
                title=f"{user.display_name} has reached level {nLevel}!",
                color=user.color
            ))

