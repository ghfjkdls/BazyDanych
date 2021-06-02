import socket
import math
import operator
import mysql.connector

def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    dioda = False

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password"
    )

    cursor = mydb.cursor()

    #cursor.execute("SHOW DATABASES")

    #for x in cursor:
        #print(x)

    cursor.execute("USE projekt")
    cursor.execute("SHOW TABLES")

    for x in cursor:
        print(x)

    cursor.execute("UPDATE terminy SET dostepnosc = 1 where id BETWEEN 1 AND 10")
    cursor.execute("select * FROM terminy")

    for x in cursor:
        print(x)

    while True:
        server_socket.listen(1)
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data == "show":
                response = "dostepne terminy: \n"
                cursor.execute("select * FROM terminy WHERE dostepnosc=1")
                for x in cursor:
                    delimeter = ', '
                    print(delimeter.join([str(value) for value in x]))
                    response += delimeter.join([str(value) for value in x])
                    response += '\n'
                conn.send(response.encode())
            elif data == "showAll":
                cursor.execute("select * FROM terminy")
                response = "wszystkie terminy: \n"
                #conn.send(response.encode())
                for x in cursor:
                    delimeter = ', '
                    print(delimeter.join([str(value) for value in x]))
                    response += delimeter.join([str(value) for value in x])
                    response += '\n'
                conn.send(response.encode())
            elif data == "book":
                cursor.execute("select * FROM terminy")
                lenght =0
                for x in cursor:
                    lenght += 1
                response = 'ktory termin'
                conn.send(response.encode())
                termin = conn.recv(1024).decode()
                if isNumber(termin):
                    term = int(termin)
                    if   term > 0 and term <= lenght:
                        response = "zgadza sie"
                        cursor.execute("UPDATE terminy SET dostepnosc = 0 where id = %s", (termin,))
                        print(response)
                        conn.send(response.encode())
                    else:
                        response = "zla wartsc"
                        print(response)
                        conn.send(response.encode())
                else:
                    response = "zla wartsc"
                    print(response)
                    conn.send(response.encode())
            else:
                response = "zle polecenie"
                print(response)
                conn.send(response.encode())



if __name__ == '__main__':


    server_program()
