import sqlite3

class GroupSQlite:

    def __init__(self, dbname="group.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS group_sqlite (chatID INTEGER, currentInterest TEXT, memberList TEXT, answered TEXT)"
        chatidx = "CREATE INDEX IF NOT EXISTS chatidx ON group_sqlite (chatID ASC)"
        currentInterestidx = "CREATE INDEX IF NOT EXISTS currentInterestidx ON group_sqlite (currentInterest ASC)"
        memberListidx = "CREATE INDEX IF NOT EXISTS memberListidx ON group_sqlite (memberList ASC)"
        answeredidx = "CREATE INDEX IF NOT EXISTS answered ON group_sqlite (answered ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(chatidx)
        self.conn.execute(currentInterestidx)
        self.conn.execute(memberListidx)
        self.conn.execute(answeredidx)
        self.conn.commit()

    def add_group(self, chatID, currentInterest, memberList, answered):
        stmt = "DELETE FROM group_sqlite WHERE chatID = (?)"
        args = (chatID, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        update_stmt = "INSERT INTO group_sqlite (chatID, currentInterest, memberList, answered) VALUES (?, ?, ?, ?)"
        update_args = (chatID, currentInterest, memberList, answered)
        self.conn.execute(update_stmt, update_args)
        self.conn.commit()

    def check_grp_interest(self, chatID):
        stmt = "SELECT currentInterest FROM group_sqlite WHERE chatID= (?)"
        args = (chatID, )
        return [x for x in self.conn.execute(stmt, args)][0][0]

    def check_answered(self, chatID):
        stmt = "SELECT currentInterest FROM group_sqlite WHERE chatID= (?)"
        args = (chatID, )
        answered = [x for x in self.conn.execute(stmt, args)][0][0]
        if answered == 'TRUE':
            return True
        else:
            return False

    def update_grp_interest(self, chatID, currentInterest):
        stmt = 'UPDATE group_sqlite SET currentInterest= (?) WHERE chatID= (?)'
        args = (currentInterest, chatID)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def update_member_list(self, chatID, memberList):
        memberstring = " ".join([str(x) for x in memberList])
        stmt = 'UPDATE group_sqlite SET memberList= (?) WHERE chatID= (?)'
        args = (memberstring, chatID)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def update_answered(self, chatID, answered):
        stmt = 'UPDATE group_sqlite SET answered= (?) WHERE chatID= (?)'
        args = (answered, chatID)
        self.conn.execute(stmt, args)
        self.conn.commit()


    def get_all_grp(self):
        stmt = 'SELECT chatID FROM group_sqlite'
        self.conn.execute(stmt)
        return [x for x in self.conn.execute(stmt)]

    def get_all_members(self, chatID):
        stmt = "SELECT memberList FROM group_sqlite WHERE chatID= (?)"
        args = (chatID, )
        members = [x for x in self.conn.execute(stmt, args)][0][0]
        members_list = [int(x) for x in members.split()]
        return members_list

    def check_available_group(self):
        memberList = ""
        stmt = "SELECT chatID FROM group_sqlite WHERE memberList= (?) LIMIT 1"
        args = (memberList,)
        chatID = [x for x in self.conn.execute(stmt, args)]
        if len(chatID) == 0:
            return False
        else:
            return True

    def get_empty_group(self):
        memberList = ""
        stmt = "SELECT chatID FROM group_sqlite WHERE memberList= (?) LIMIT 1"
        args = (memberList,)
        chatID = [x for x in self.conn.execute(stmt, args)]
        if len(chatID) == 0:
            return 0
        else:
            return chatID[0][0]