import sqlite3
try:
    sqliteConnection = sqlite3.connect('db.sqlite3')
    sqlite_create_table_query = '''CREATE TABLE Vehicle_Parkings (
                                plate_number TEXT NOT NULL,
                                vehicle_type INTEGER NOT NULL,
                                parking_spot INTEGER NOT NULL,
                                entry_time datetime NOT NULL,
                                exit_time datetime);'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")
