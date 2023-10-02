from django.shortcuts import render
from django.http import HttpResponse
from .models import Parkings
import datetime
import sqlite3
import delete

def readSqliteTable(plate_number):
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from Vehicle_Parkings where plate_number = ?"""
        cursor.execute(sqlite_select_query, (plate_number,))
        record = cursor.fetchone()
        if (record == None):
            return None
        entry = datetime.datetime.strptime(record[3], '%Y-%m-%d %H:%M:%S.%f')
        
        if (record[4] != None):
            exit_time = datetime.datetime.strptime(record[4], '%Y-%m-%d %H:%M:%S.%f')
        else:
            exit_time = record[4]
        
        vehicle = (record[0], record[1], record[2], entry, exit_time)
        # print("Plate Number: ", record[0])
        # print("Vehicle type: ", record[1])
        # print("Parking Spot: ", record[2])
        # print("Entry time: ", record[3])
        # print("Exit time: ", record[4])
        cursor.close()
        return vehicle

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        

# Create your views here.
def index(request):
    return render(request, "parking/index.html")

def details(request, number):
    if request.method == "POST":
        if "yes" in request.POST:
            plate_number = number.split()
            print(f"Number: {plate_number[3]}")
            delete.delete(plate_number[3])
            return render(request, "parking/thank_you.html")
        #vehicle = Parkings.objects.get(plate_number=request.POST.get("plate_number"))
        vehicle = readSqliteTable(request.POST.get("plate_number"))
        if (vehicle == None):
            return render(request, "parking/error.html")
        if vehicle[4] != None:
            duration = vehicle[4] - vehicle[3]
            if (duration.seconds//3600) < 2:
                amount = 50
            else:
                hour = (duration.seconds//3600) - 1
                amount = 50 + hour * 50

        else:
            duration = 0
            amount = 0
    
        return render(request, "parking/details.html", {
            "vehicle" : vehicle,
            "plate_number" : vehicle[0],
            "vehicle_type" : vehicle[1],
            "parking_spot" : vehicle[2],
            "entry_time" : vehicle[3],
            "exit_time" : vehicle[4],
            "duration" : duration,
            "amount" : amount
        })
        #return HttpResponse(f"{vehicle}")