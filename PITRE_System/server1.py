import socket 
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server1_address = ('192.168.215.128', 9992)
print("\n--------------- TRE SERVER (SERVER-1) ---------------")
s.bind(server1_address)
s.listen(1)
print("\nWaiting for connection")

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2_address = (('192.168.215.129'), 9993)
s2.connect(server2_address)

def receive():  
    c,addr = s.accept()
    print("Connection from: " + str(addr))
    
    while True:
        data = c.recv(1024)
        if data:
            print("\n-- Received data from client")
            userInfo = []
            taxInfo = []
            clientTfn, userInfo = pickle.loads(data)        #unpack the received data
            if clientTfn == "no":
                print("-- Calculating tax estimate")
                taxInfo = calculateTax(userInfo)            #pass the received data to calculateTax function to calculate the tax charges
                print("-- Returning tax estimate results to client")
                c.sendall(pickle.dumps(taxInfo))           #return tax results to client             
            else:
               print("-- Sending information of TFN user to server-2")
               s2.sendall(pickle.dumps(userInfo))           #send received data to server-2
               receivedData = s2.recv(1024)             
               if receivedData:
                  print("-- Received tax related data from server-2")
                  userInfo = pickle.loads(receivedData)     #unpack the data received from server-2 into a list
                  if type(userInfo) == list :
                        print("-- Calculating tax estimate for user with TFN")
                        taxInfo = calculateTax(userInfo)     #pass the received data to calculateTax function to calculate the tax charges
                        print("-- Returning tax estimate results to client")
                        c.sendall(pickle.dumps(taxInfo))    #return tax results to client
                  else:
                        print("--Sending TFN not found message to client")
                        c.sendall(pickle.dumps(userInfo))
               else:
                    print("-- No data received from server 2. CONNECTION CLOSED.")
                    s2.close()
        else:
            print("-- No data received from client. CONNECTION CLOSED.")
            c.close()
            break

def calculateTax(wagelist):
    
    tfn = wagelist[0] 
    personID = wagelist[1] 
    taxInfo = []

    i = 2
    biweeklyWagesTotal = 0
    taxWithheldTotal = 0
    medicareLevy = 0
    tax = 0
    medicareLevySurcharge = 0
    netIncome = 0
    taxReturn = 0
    
    #calculate total biweekly wages and tax withheld
    while i < (len(wagelist) - 1):
       biweeklyWagesTotal = biweeklyWagesTotal + float(wagelist[i])
       taxWithheldTotal = taxWithheldTotal + float(wagelist[i+1])
       i = i + 2
    
    #calculate tax
    if biweeklyWagesTotal >= 0 and biweeklyWagesTotal <= 18200:
        tax = 0
    elif biweeklyWagesTotal >= 18201 and biweeklyWagesTotal <= 45000:
        tax = (biweeklyWagesTotal - 18200) * 0.019
    elif biweeklyWagesTotal >= 45001 and biweeklyWagesTotal <= 120000:
        tax = 5092 + ((biweeklyWagesTotal - 45000) * 0.325)
    elif biweeklyWagesTotal >= 120001 and biweeklyWagesTotal <= 180000:
        tax = 20467 + ((biweeklyWagesTotal - 120000) * 0.370)
    else:
        tax = 51667 + ((biweeklyWagesTotal - 180000) * 0.450)
    
    #calculate medicare levy
    medicareLevy = biweeklyWagesTotal * 2/100
    
    #calculate medicare levy surcharge
    if wagelist[len(wagelist) - 1] == "no":
        if biweeklyWagesTotal >= 0 and biweeklyWagesTotal <= 90000:
            medicareLevySurcharge = 0
        elif biweeklyWagesTotal >= 90001 and biweeklyWagesTotal <= 105000:
            medicareLevySurcharge = biweeklyWagesTotal * 1/100
        elif biweeklyWagesTotal >= 105001 and biweeklyWagesTotal <= 140000:
            medicareLevySurcharge = biweeklyWagesTotal * 1.25/100    
        else:
            medicareLevySurcharge = biweeklyWagesTotal * 1.5/100  
    
    #calculate net income
    netIncome = biweeklyWagesTotal - (tax + medicareLevy + medicareLevySurcharge)
    
    #calculate tax return
    taxReturn = taxWithheldTotal - (tax + medicareLevy + medicareLevySurcharge)
    
    #combine all the tax result information into one list
    taxInfo = [tfn, personID, biweeklyWagesTotal, taxWithheldTotal, netIncome, taxReturn]
    return taxInfo

receive() 
