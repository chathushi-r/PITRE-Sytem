
import socket
import pickle

#create a socket and connect to server-1
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.215.128', 9992)
c.connect(server_address)

def main():
    login()         #call login function
    
def login():

    print("\n -------------- WELCOME TO PITRE SYSTEM -----------------")   #welcome message
    
    count = 0                                                  #variable to store number of times loop iterates
    users = {"client": "clntaccess","admin":"admaccess"}        #dictionary to store user accounts
    validUser = False                                           #a variable to denote if the user is valid/not
    
    print("\n Please login:")
    while count < 3:                                           #loop iterates till number of login attempts = 3
        username = input("\n Enter username: ")                  #user input username
        password = input(" Enter password: ")                    #user input password
        for user,password in users.items():                     #loop through dictionary items
            if username == user and password == password:       
                validUser = True                                #if login info is valid, set the variable as True
                break       #exit loop
        if validUser:           #if the user is a valid user
            print("\n --Authentication successful.")
            optionMenu()
            break
        else:
            print("\n --Authentication unsuccessful. Please check login credentials.")
            count += 1          #increment count by 1
    
    if validUser == False:      #if user is not valid after maximum number of attempts
        print("\n --Number of attempts over. Please try again later.")
        
def checkTFN():
    while True:
        #check if the user have a TFN or not
        clientTfn = input("\n Do you have a tax file number TFN (yes/no)? ")
        if clientTfn == "yes" or clientTfn == "no":
            getUserInfo(clientTfn)       #function call
            break
        else:
            print("\n --Incorrect choice. Please enter yes/no.")     #if the user inputs something other than yes/no
  
def getUserInfo(clientTfn):
    #msg = ""
    userInfo = []
    if clientTfn == "yes":          #if the user has a TFN
        
        while True:
            tfnNo = input("\n Enter tax file number (TFN): ")              #user input tfn
            if int(tfnNo) >= 100000000 and int(tfnNo) < 1000000000:     #checks if the TFN is a 9 digit number
                break
            else:
                print("\n --Incorrect TFN. Please enter a valid 9-digit TFN.")
        
        #input other user information to authenticate the user's TFN
        print("\n For authentication purposes, please enter following details.")
        while True:
            personID = input(" Enter person id: ")
            if int(personID) >= 100000000 and int(personID) < 1000000000:
                break
            else:
                print("\n --Incorrect Person id. Please enter a valid 9-digit person id.")
        
        while True:
            firstName = input(" Enter first name: ")
            lastName = input(" Enter last name: ")
            if firstName.isalpha() and lastName.isalpha():
                break
            else:
                print("\n --Invalid name formats. Please enter valid first name and last name.\n")
                
        emailAddress = input(" Enter email address: ")
        
        userInfo = [tfnNo, personID, firstName, lastName, emailAddress]
              
    else:      #if the user does not have a TFN
        tfnNo = "No TFN"
        
        while True:
            personID = input(" Enter person id: ")
            if int(personID) >= 100000000 and int(personID) < 1000000000:
                break
            else:
                print("\n --Incorrect Person id. Please enter a valid 9-digit person id.") 
        
        userInfo = [tfnNo, personID]
        i = 1
        
        print("\n Enter biweekly wages and tax withheld. Max is 26 items or enter 0 if you are done.")
        while True:
            if i > 26:
                print("\n Maximum 26 items.")
                break;
            else:
                print("",i,")")
                wage = input(" Enter net wage and corresponding tax withheld pair (Eg: 50200, 8735): ")
                if wage == '0':
                    break
                else:
                    netWage,taxWithheld = wage.split(", ")      #split the inputted wage pair into two variables
                    if taxWithheld < netWage:       #check taxwithheld is less than net wage
                        userInfo.append(netWage)
                        userInfo.append(taxWithheld)
                        i += 1
                    else:
                        print("\n --Invalid tax withheld amount. Taxwithheld should be less than net wage. ")
        
    while True: 
        privateHealthIns = input("\n Do you have a Private Health Insurance cover (yes/no)?");   #user input if they have a insurance cover
        if privateHealthIns == "yes" or privateHealthIns == "no":
            userInfo.append(privateHealthIns)
            break
    getTaxResult(clientTfn, userInfo)
    

def getTaxResult(clientTfn, userInfo):
    #send clientTfn and user information list to server 1
    c.sendall(pickle.dumps((clientTfn, userInfo)))
   
    #receives the tax estimate reults from server-1
    data = c.recv(1024)
    print("\n -------------------- Tax Extimate Result --------------------")
    if data:        #if data is received
        taxInfo = []
        taxInfo = pickle.loads(data)
        if type(taxInfo) == list:
            TFN,personID,annualIncome,totalTaxWithheld,netIncome,taxRefund = taxInfo
            print("\n Person ID: ", personID)
            print(" Tax File Number: ",TFN)
            print(" Annual Taxable Income: ",annualIncome)
            print(" Total Tax Withheld: ",totalTaxWithheld)
            print(" Total Net Income: ",netIncome)
            print(" Estimated Tax Refund: ",taxRefund)
        else:
            print("\n",taxInfo)     #display error message if the TFN is not available in the database
    else:
        print("\n --No data")
    print("\n -------------------------------------------------------------")
    
    optionMenu()

def optionMenu():
    while True:
        print("\n 1) Do you want to calculate tax estimate? \n 2) Exit the program")
        option = input("\n Enter option: ")
        if int(option) == 1:
            checkTFN()
            break
        elif int(option) == 2:
            print("\n ------------- THANK YOU FOR USING THE PITRE SYSTEM -----------")
            c.close()
            break
        else:
            print("\n --Invalid option. Please enter 1 or 2.")
    
  
if __name__=="__main__":
    main()