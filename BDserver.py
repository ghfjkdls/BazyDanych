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

    master = mysql.connector.connect(
      host='192.168.1.42',
      user='remote',
      password='password',
      auth_plugin='mysql_native_password',
      autocommit=True
    )

    cursorMaster = master.cursor()


    slave = mysql.connector.connect(
      host='192.168.1.44',
      user='remoteread',
      password='password',
      auth_plugin='mysql_native_password'
    )

    cursorSlave = slave.cursor()

    #cursor.execute("SHOW DATABASES")

    #for x in cursor:
        #print(x)

    cursorMaster.execute("USE projekt")
    cursorSlave.execute("USE projekt")
    cursorMaster.execute("SHOW TABLES")

    for x in cursorMaster:
        print(x)

    #cursorMaster.execute("UPDATE terminy SET dostepnosc = 1 where id BETWEEN 1 AND 10")
    #master.commit()
    cursorMaster.execute("select * FROM terminy")

    for x in cursorMaster:
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
                cursorSlave.execute("select * FROM terminy WHERE dostepnosc=1")
                for x in cursorSlave:
                    delimeter = ', '
                    print(delimeter.join([str(value) for value in x]))
                    response += delimeter.join([str(value) for value in x])
                    response += '\n'
                conn.send(response.encode())
            elif data == "showAll":
                cursorSlave.execute("select * FROM terminy")
                response = "wszystkie terminy: \n"
                #conn.send(response.encode())
                for x in cursorSlave:
                    delimeter = ', '
                    print(delimeter.join([str(value) for value in x]))
                    response += delimeter.join([str(value) for value in x])
                    response += '\n'
                conn.send(response.encode())
            elif data == "book":
                cursorMaster.execute("select * FROM terminy")
                lenght =0
                for x in cursorMaster:
                    lenght += 1
                response = 'ktory termin'
                conn.send(response.encode())
                termin = conn.recv(1024).decode()
                if isNumber(termin):
                    term = int(termin)
                    if   term > 0 and term <= lenght:
                        response = "zgadza sie"
                        cursorMaster.execute("UPDATE terminy SET dostepnosc = 0 where id = %s", (termin,))
                        master.commit()
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
