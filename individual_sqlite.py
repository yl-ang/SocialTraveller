# Put your code here

import sqlite3

class IndividualSQite:

    """
    A class to create a database to store individual's chat id and their interest tags.
    
    ...
    Attributes
    ----------
    dbname : str
        The name of the sqlite file to open

    Methods
    -------
    setup():
        Create the table individual_DB if not exist for storage and retrieval of data. 
        create the Virtrual table match_DB for searching of users with common tags.
    
    add_chatID_tags(chatID, tags):
        Add the user chat id and the interest tags into the individual_DB table.
    
    add_tags(chatID, tags):
        Add additional tags to an existing chat id on the individual_DB table.
    
    remove_tags(chatID, tags):
        Remove tags from an exisitng chat id on the individual_DB table.

    get_tags(chatID):
        Retrieve the tags to a chat id from the individual_DB table.
    
    count_users():
        Retrieve the number of chat ids from the individual_DB table.

    match_users(random_interest):
        Retrieves a list of users with the common interest from the match_DB Virtual Table.

    """

    def __init__(self, dbname="individual.sqlite"):

        """
        Constructs all the necessary attributes for the IndividualSQite db objects
        Parameters
        ----------
            dbname : str
                Name of the sqlite file to open/read/write
        """
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        
        """
        Creates the table individual_DB in the sqlite file if not exist
        Creates the virtual table match_DB in the sqlite file if not exist

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        """

        tblstmt = "CREATE TABLE IF NOT EXISTS individual_DB (chatID INTEGER, tags TEXT)"
        chatidx = "CREATE INDEX IF NOT EXISTS chatidx ON individual_DB (chatID ASC)"
        tagsidx = "CREATE INDEX IF NOT EXISTS tagsidx ON individual_DB (tags ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(chatidx)
        self.conn.execute(tagsidx)

        # Add fts5 table for searching purposes
        self.conn.execute('DROP TABLE IF EXISTS match_DB')
        self.conn.execute('CREATE VIRTUAL TABLE IF NOT EXISTS match_DB USING fts5 (chatID, tags, tokenize = "porter ascii")')
        self.conn.commit()
    
    def add_chatID_tags(self, chatID, tags):

        """
        Add chat id and interest tags into the individual_DB splite table.

        Parameters
        ----------
            chatID : int
                The chat id to add into the individual_DB database.
            tags : str
                The tags to add into the individual_DB databse.

        Returns
        -------
        None
        
        """
        stmt = "DELETE FROM individual_DB WHERE chatID = (?)"
        args = (chatID, )
        self.conn.execute(stmt, args)
        update_stmt = "INSERT INTO individual_DB (chatID, tags) VALUES (?, ?)"
        update_args = (chatID, tags)
        self.conn.execute(update_stmt, update_args)
        self.conn.commit()

    def add_tags(self, chatID ,tags):

        """
        Add interest tags into the individual_DB splite table based on the chat id.

        Parameters
        ----------
            chatID : int
                The chat id to retrive the interest tags from the individual_DB.
            tags : str
                The tags to add into the individual_DB databse.

        Returns
        -------
        None
        
        """

        get_tags_stmt = "SELECT tags FROM individual_DB WHERE chatID= (?)"
        get_tags_args = (chatID,)
        queried_tags =  [x for x in self.conn.execute(get_tags_stmt, get_tags_args)][0][0] # list
        lst_tags = tags.split()
        update_tags = queried_tags.split() + lst_tags
        update_tags = " ".join(update_tags)
        print(update_tags)
        update_tags_stmt = "UPDATE individual_DB SET tags = (?) WHERE chatID = (?)"
        update_tags_args = (update_tags, chatID)
        self.conn.execute(update_tags_stmt, update_tags_args)
        self.conn.commit()
    
    def remove_tags(self, chatID, tags):
        
        """
        Remove interest tags from the individual_DB splite table based on the chat id.

        Parameters
        ----------
            chatID : int
                The chat id to retrive the interest tags from the individual_DB.
            tags : str
                The tags to remove from the individual_DB databse.

        Returns
        -------
        None
        
        """

        get_tags_stmt = "SELECT tags FROM individual_DB WHERE chatID= (?)"
        get_tags_args = (chatID,)
        queried_tags = [x for x in self.conn.execute(get_tags_stmt, get_tags_args)][0][0] # list
        lst_tags = tags.split()
        queried_tags = [x for x in queried_tags.split() if x not in lst_tags] # list comprehension to remove tags from queried tags
        update_tags = " ".join(queried_tags)
        print(update_tags)
        update_tags_stmt = "UPDATE individual_DB SET tags = (?) WHERE chatID = (?)"
        update_tags_args = (update_tags, chatID)
        self.conn.execute(update_tags_stmt, update_tags_args)
        self.conn.commit()

    def get_tags(self, chatID):

        """
        Retrieve interest tags from the individual_DB splite table based on the chat id.

        Parameters
        ----------
            chatID : int
                The chat id to retrive the interest tags from the individual_DB.
            tags : str
                The tags to remove from the individual_DB databse.

        Returns
        -------
            tags (str) : Retrieved interest tags from the individual_DB.
        
        """
        get_tags_stmt = "SELECT tags FROM individual_DB WHERE chatID= (?)"
        get_tags_args = (chatID,)
        return [x for x in self.conn.execute(get_tags_stmt, get_tags_args)][0][0].split()

    def count_users(self):
        """
        Retrieves the number of users from the individual_DB.

        Parameters
        ----------
        None

        Returns
        -------
            len(result) (int) : Number of users.
        
        """
        count_stmt = "SELECT chatID FROM individual_DB"
        result = [x for x in self.conn.execute(count_stmt)]
        return len(result)

    def match_users(self, random_interest):
        """
        Retrieves the number of users from the individual_DB.

        Parameters
        ----------
            random_interest (str) : A random interest tag.

        Returns
        -------
            result (list) : A list of users with the common interest tag.
        
        """
        # Get all the people with the same interest
        self.conn.execute('INSERT INTO match_DB SELECT chatID, tags FROM individual_DB;')
        match_stmt = "SELECT chatID FROM match_DB WHERE tags MATCH ?"
        match_args = (random_interest,)
        result = [x for x in self.conn.execute(match_stmt, match_args)]
        return result
