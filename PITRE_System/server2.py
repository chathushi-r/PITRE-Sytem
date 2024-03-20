import socket 
import pickle
import pyodbc

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2_address = ('192.168.215.129', 9993) 
print("\n---------------- PITD SERVER (SERVER-2) ----------------")
s.bind(server2_address)
s.listen(1)
print("\nWaiting for connection")
c,addr = s.accept()
print("\nConnection from: " + str(addr))

#declare sql server details
SQL_ServerName = "DESKTOP-V11REUR\SQLEXPRESS"
SQL_ServerDB = "employeeTax"
SA2_PORT = 51515

def receive():
    while True:
        data = c.recv(1024)
        if data:
            employeeInfo = []
            employeeInfo = pickle.loads(data)   #unpack the data received from server-1
            print("\n-- Received employee TFN data from server-1")
            tfnNo = employeeInfo[0]
            personID = employeeInfo[1]
            firstName = employeeInfo[2]
            lastName = employeeInfo[3]
            emailAddr = employeeInfo[4]
            
            getTaxData(tfnNo, personID, firstName,lastName,emailAddr)
        else:
            print("\n-- No data received. CONNECTION CLOSED.")
            break

def sqlQuery(q, args):
    #connect to the database
    connection = pyodbc.connect('Driver={SQL Server};'
                                'Server='+SQL_ServerName+';'
                                'Database='+SQL_ServerDB+';'
                                'Trusted_Connection=yes;')
    cursor = connection.cursor()
    cursor.execute(q, args)
    return cursor
   

def getTaxData(tfnNo,personID, firstName,lastName,emailAddr):
    print("-- Checking for employee details")
    employeeData = list()
    print("-- Performing a database lookup for the received TFN")
    print("-- Authenticating the received TFN user information")
    cursor = sqlQuery('SELECT tfnNO, personID, firstName, lastName, email FROM employeeInfo WHERE tfnNO = ? AND personID = ? AND firstName = ? AND lastName = ? AND email = ?', [tfnNo, personID, firstName, lastName, emailAddr])
    for i in cursor:
        employeeData.append( [i[0], i[1]] )         #append query results to a list
               
    if len(employeeData) == 0:
        print("-- Invalid TFN not found in the database")
        empPayInfo = "Invalid TFN not found in the database."
        c.sendall(pickle.dumps(empPayInfo))         #return invalid message to server-1
    else:
        print("-- Valid TFN found in the database")
        wageData = list()
        print("-- Retrieving TFN's payroll records")
        cursorList = sqlQuery('SELECT biweeklyWage, taxWithheld FROM payrollInfo WHERE tfnNo = ?', [tfnNo])
        for i in cursorList:
            wageData.append([i[0],i[1]])        #append tax records of that specific TFN no to a list
        
        if len(wageData) == 0:
            empPayInfo = "TFN found in the database but no payroll records found."
            c.sendall(pickle.dumps(empPayInfo))
        else:
            empPayInfo = [tfnNo,personID]
            i = 0
            while i < len(wageData):
                empdata = str(wageData[i]).replace("[","")
                empdata = empdata.replace("]","")
                empdata = empdata.replace("'","")
                biweeklyPay, taxWithheld = empdata.split(", ")
                empPayInfo.append(biweeklyPay)
                empPayInfo.append(taxWithheld)
                i = i + 1       
            print("-- Sending TFN user's tax related data to server-1 ")
            c.sendall(pickle.dumps(empPayInfo))     #send tax records to server-1
    
receive()