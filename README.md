**Personal Income Tax Return Estimate System**

This repository contains source codes for a small distributed system for a Personal Income Tax Return Estimate system, implemented in Python. 

This system consists of a 3-tiered client-server architecture that allows taxpayers to calculate their tax returns. The client and servers' components are designed to run on separate machines, implemented using virtualization. 
Connections between the different virtual machines are established with the use of socket programming in Python. Considering the processes between the components, a message oriented system along with Remote Procedure Call (RPC) technique 
is used to pass parameters in messages and call functions accordingly.

**Functionalities:**

- Client: Acts as the individual’s tax return estimate client. It can be used by a taxpayer to log in to the system and input their tax information to receive a tax return estimate.
          Thereafter, the client component gathers the data entered by the user and transmits it to a remote application in server 1.
- Server 1: Acts as the server-side application which will authenticate the received data from client. 
          Based on the data received, server 1 will perform one of the following functions. If the user does not have a tax file number (TFN), the server 1 component will estimate the tax return based on the                   payroll records inputted and provide the estimate result to the client. If the user has a tax file number (TFN), Server 1 will request tax-related records for the specified tax file number (TFN) from 
          Server 2, the database server. After receiving the tax related data, server 1 will compute the tax return estimate and return the result to the client.
               
- Server 2: Acts as the database server, which is responsible for storing tax related records of taxpayers.

**Technologies used:**
- Language: Python
- Text Editor: VS Code
- Database: MSSQL
- Virtualization - VMware
