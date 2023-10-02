import sqlite3
import datetime

def updateSqliteTable(plate_number):
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        exit = datetime.datetime.now()
        sql_update_query = """Update Vehicle_Parkings set exit_time = ? where plate_number = ?"""
        data = (exit, plate_number)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

updateSqliteTable("KA05MJ1721")
