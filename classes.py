import psycopg2
import os


class Database:
    
    def __init__(self, connection):
        self.connection = connection

    def AddItemToList(self, item, user):
        item = item.replace("'", "''")
        cursor = self.connection.cursor()
        cursor.execute(f"""
                            INSERT INTO list(id, author, item)
                            VALUES (DEFAULT, '{user}', '{item}');
                       """)
        self.connection.commit()
        self.Renum()
        cursor.close()

    def GetList(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM list;""")
        result = ''
        for item in cursor:
            result += str(item[0]) + '. ' + str(item[2]) + '\n'
        cursor.close()
        if result == '':
            return 'List is empty.'
        return result

    def DeleteFromList(self, id):
        cursor = self.connection.cursor()
        cursor.execute(f"""
                        DELETE FROM list
                        WHERE id = {id};
                       """)
        self.connection.commit()
        cursor.close()
        self.Renum()

    def CreatDB(self):
        cursor = self.connection.cursor()
        cursor.execute("""DROP TABLE list;""")
        cursor.execute("""
        CREATE TABLE list
                      (
                        id        SERIAL          PRIMARY KEY      NOT NULL,
                        author    VARCHAR(100)                             ,
                        item      VARCHAR(10000)                           
                      );
                      """)
        self.connection.commit()
        cursor.close()

    def Renum(self):
        cursor = self.connection.cursor()
        updator = self.connection.cursor()
        cursor.execute("""
                        SELECT id
                        FROM list
                        ORDER BY id;
                      """)
        n = 0
        for i in cursor:
            n += 1
            updator.execute(f"""UPDATE list SET id = {n}
                               WHERE id = {i[0]};""")
        self.connection.commit()
        updator.close()
        cursor.close()
    
def DatabaseVars(connect_string):
    i = 0
    connection = {
        'user': '',
        'password': '',
        'host': '',
        'port': '',
        'database': ''
    }
    condition = 'None'

    while i < len(connect_string):

        if connect_string[i] == '/':
            if connect_string[i - 1] == '/':
                condition = 'user'
            else:
                condition = 'database'
                
        elif connect_string[i] == ':' and condition == 'user':
            condition = 'password'
            
        elif connect_string[i] == '@' and condition == 'password':
            condition = 'host'
            
        elif connect_string[i] == ':' and condition == 'host':
            condition = 'port'
            
        elif condition != 'None':
            connection[condition] += connect_string[i]
        i += 1
    return connection

def GetDelIndex(string):
    string = string.lower().replace(" ", "").replace("del", "")

    if string.isdecimal() == False or string.isdigit() == False:
        return ''
    return int(string)

def IsAdmin(admins, user):
    for admin in admins:
        if user == admin:
            return True
    return False

def AdminList():
    admins = str(os.environ['ADMINS']).split(r',')
    for i in range(0, len(admins)):
        admins[i] = int(admins[i])
    return admins