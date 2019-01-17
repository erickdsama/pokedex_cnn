import sqlite3

def exec_command(command):
    db = sqlite3.connect('index.db')
    cursor = db.cursor()
    cursor.execute(command)
    db.commit()
    db.close()


def create_table(db=None):
    command = '''
        CREATE TABLE IF NOT EXISTS class_index(id INTEGER PRIMARY KEY, index_class INTEGER, class_name TEXT);
    '''
    exec_command(command)


def truncate_table(db=None):
    exec_command('''
        delete from class_index;
    ''')


def insert(indexes, db=None):
    if not db:
        db = sqlite3.connect('index.db')
    create_table(db=db)
    truncate_table(db=db)

    cursor = db.cursor()
    print("aqui andox")
    for class_name, index in indexes.items():
        cursor.execute('''INSERT INTO class_index(index_class, class_name)
                  VALUES(?,?)''', (index, class_name))
    db.commit()
    db.close()


def get_class_by_index(index):
    db = sqlite3.connect('index.db')
    cursor = db.cursor()
    data = cursor.execute("select * from class_index where index_class={}".format(index))
    pokemon = data.fetchone()
    db.close()
    if not pokemon:
        return "Index not found!"
    return pokemon[2]
