from __future__ import print_function
from wsgiref.handlers import format_date_time

import threading

import logging
import datetime as dt
import utils as utils
import sys

import grpc
import safe_entry_pb2 as se_pb2
import safe_entry_pb2_grpc as se_pb2_grpc

# replace address with server ip if connecting to other PC within the network
address = 'localhost'

# A class for handling client
class Client(object):
    # Initialisation
    def __init__(self, nric):
        self.nric = nric
        self.name = None

        # create a gRPC channel to connect to server 
        self.channel = grpc.insecure_channel(address + ':50051')
        # create a gRPC stub to communicate to server
        self.stub = se_pb2_grpc.SafeEntryStub(self.channel)

        # login to server and retrieve user's name
        response = self.stub.Login(se_pb2.LoginRequest(nric=nric))
        if response:
            if response.status == se_pb2.Status.SUCCESS:
                self.name = response.name
                print("Login successfully!\n")
            else:
                print("Login fail...\n")
        else:
            print("Some error has occur...\n")
    
        # check if user has notification message(s) for possible exposure of covid and notify them
        response = self.stub.NotificationCheck(se_pb2.NRIC(nric=self.nric))
        for msg in response.message:
            print(msg) 

        # create a thread to listen for new incoming notification message(s) stream
        threading.Thread(target=self.__listen_for_notifications, daemon=True).start()

    # This function will run in a separated thread to listen for incoming notification message(s) stream
    def __listen_for_notifications(self):
        for noti in self.stub.SubscribeNotification(se_pb2.NRIC(nric=self.nric)):
            print(noti.message)
        
    # Single check in
    def SingleCheckIn(self):
        # send request to check if user has not check in from previous (single/group) location
        request = se_pb2.NRIC(nric=self.nric)
        response = self.stub.CheckForStatus(request)

        # if previous location was already check out, do a new check in for new location
        if response.status == se_pb2.Status.SUCCESS:
            location = input("Enter location: ")

            # convert current date and time formatting
            date = dt.datetime.now().strftime(utils.format_date)
            checkin_time = dt.datetime.now().strftime(utils.format_time)
            
            # send request for single check in
            request1 = se_pb2.CheckRequest(user=se_pb2.User(nric=self.nric),
            date=date,
            location=location,
            checkin_time=checkin_time)
            
            response1 = self.stub.SingleCheckIn(request1)

            if response1.status == se_pb2.Status.SUCCESS:
                print("Check in successfully!\n")
            elif response1.status == se_pb2.Status.FAILURE:
                print("Check in unsuccessful...\n")
            else:
                print("Some error has occur...\n")
        # if previous location was not check out yet for Single
        elif response.status == se_pb2.Status.SFAILURE:
            print("Single check in unsuccessful...Please do Single check out for previous location first!\n")
        # if previous location was not check out yet for Group
        elif response.status == se_pb2.Status.GFAILURE:
            print("Single check in unsuccessful...Please do Group check out for previous location first!\n")
        else:
            print("Some error has occur...\n")

    # Single check out
    def SingleCheckOut(self):
        # send request to check if user has not check in from previous (single/group) location
        request = se_pb2.NRIC(nric=self.nric)
        response = self.stub.CheckForStatus(request)

        # if previous location was not check out yet for Single
        if response.status == se_pb2.Status.SFAILURE:
            # convert current time formatting
            checkout_time = dt.datetime.now().strftime(utils.format_time)

            # send request for single check out
            request1 = se_pb2.CheckRequest(user=se_pb2.User(nric=self.nric),
            checkout_time=checkout_time)
            response1 = self.stub.SingleCheckOut(request1)
            
            if response1.status == se_pb2.Status.SUCCESS:
                 print("Check out successfully!\n")
            elif response1.status == se_pb2.Status.FAILURE:
                print("Check out unsuccessful...\n")
            else:
                print("Some error has occur...Please try again...\n")

        # if previous location was not check out yet for Group
        elif response.status == se_pb2.Status.GFAILURE:
            print("Single check out unsuccessful...Please do Group check out for previous location first!\n")
        # if user is not check in to any location yet
        elif response.status == se_pb2.Status.SUCCESS:
            print("Single check out unsuccessful...You have not check in to any location yet....\n")
        else:
            print("Some error has occur...Please try again...\n")
     
    # Group check in
    def GroupCheckIn(self):
        arr = []
        nricList = []
        count = 0
        # limit user input to a number > 1
        while count <= 1:
            count = int(input("Enter how many family members(including youself >1): "))
        
        # convert current date and time formatting
        date = dt.datetime.now().strftime(utils.format_date)
        checkin_time = dt.datetime.now().strftime(utils.format_time)

        location = input("Enter location: ")

        # loop through the number of family members for their NRIC
        # person 1 should be yourself
        for i in range(count):
            nric = input(f"Enter NRIC for person {i+1}: ")

            # store inputs in list         
            arr.append(se_pb2.CheckRequest(user=se_pb2.User(nric=nric),
            date=date,
            location=location,
            checkin_time=checkin_time))
            nricList.append(se_pb2.NRIC(nric=nric))
        
        # send request to check if any family members has not check out from previous location
        request = se_pb2.NRICList(nric=nricList)
        response = self.stub.CheckForGroupStatus(request)

        # if all family members previous location was already check out, do a new check in for new location
        if response.status == se_pb2.Status.SUCCESS:
            # send request for group check in
            response1 = self.stub.GroupCheckIn(se_pb2.GroupCheckRequest(checkRequest=arr,nric=nricList))
            if response1.status == se_pb2.Status.SUCCESS:
                print("Group Check in successfully!\n")
            else:
                print("Group Check in unsuccessful...\n")
        # if family member previous location was not check out yet, display those who are required to check out
        elif response.status == se_pb2.Status.FAILURE:
            converted_list = [str(element) for element in response.name]
            name_list = ",".join(converted_list)
            print("Group Check in unsuccessful...Please ask {} to check out from previous location first!\n".format(name_list))
        else:
            print("Some error has occur...Please try again...\n")
 
    # Group check out
    def GroupCheckOut(self):
        # send request to check if user has not check in from previous (single/group) location
        request = se_pb2.NRIC(nric=self.nric)
        response = self.stub.CheckForStatus(request)

        # if previous location was not check out yet for Group
        if response.status == se_pb2.Status.GFAILURE:
            # convert current time formatting
            checkout_time = dt.datetime.now().strftime(utils.format_time)

            # send request for group check out
            request = se_pb2.CheckRequest(user=se_pb2.User(nric=self.nric),
                checkout_time=checkout_time)
            response = self.stub.GroupCheckOut(request)

            if response.status == se_pb2.Status.SUCCESS:
                print("Group Check out successfully!\n")
            else:
                print("Group Check out unsuccessful...\n")
        # if previous location was not check out yet for Single
        elif response.status == se_pb2.Status.SFAILURE:
            print("Group Check out unsuccessful...Please do single check out for previous location first!\n")
        # if user is not check in to any location yet
        elif response.status == se_pb2.Status.SUCCESS:
            print("Group Check out unsuccessful...You have not check in any location yet....\n")
        else:
            print("Some error has occur...Please try again...\n")

    # List user's history records
    def ListHistory(self):
        request = se_pb2.HistoryRequest(nric=self.nric)
        print("+-------------------------------------------------------------------+")
        print("|-----------------------------History List--------------------------|")
        print("+----------------+----------------+----------------+----------------+")
        print("|Date            |Location        |Checkin time    |Checkout time   |")
        print("+----------------+----------------+----------------+----------------+")
        response = self.stub.ListHistory(request)
        space = ' '
        max_space = 16
        if not response.historyListResponse:
                print("|                        No records Found!                          |")

        for resp in response.historyListResponse:
            print(f"|{resp.date}{abs(max_space-len(resp.date))*space}|{resp.location}{abs(max_space-len(resp.location))*space}|{resp.checkin_time}{abs(max_space-len(resp.checkin_time))*space}|{resp.checkout_time}{abs(max_space-len(resp.checkout_time))*space}|")
        
        print("+----------------+----------------+----------------+----------------+\n")

    # MOH Officer function to declare location have been visited by covid
    def NotifyCovidCase(self):
        date = input("Enter date(DD/MM/YYYY): ")
        time = input("Enter time(HH:MM(AM/PM)): ")
        location = input("Enter location: ")
        
        response = self.stub.NotifyCovidCase(se_pb2.NotificationRequest(date=date, time=time, location=location))
        if response.status == se_pb2.Status.SUCCESS:
            print("Declared successfully!\n")
    
    # Logout
    def Logout(self):
        # send request to logout from server and exit the client
        response = self.stub.Logout(se_pb2.LoginRequest(nric=self.nric))

        if response:
            if response.status == se_pb2.Status.SUCCESS:
                print("Logout successfully!\n")
            else:
                print("Logout failed...\n")
        else:
            print("Some error has occur...\n")
        
        sys.exit()

    # load json file for testing purposes
    def LoadJSONFile(self):
        filename = input("Enter JSON filename: ")
        response = self.stub.LoadJSONFile(se_pb2.Filename(filename=filename))

        if response:
            if response.status == se_pb2.Status.SUCCESS:
                print("Loaded successfully!\n")
            else:
                print("Load failed...\n")
        else:
            print("Some error has occur...\n")

    # Run client menu
    def Run(self):
        if (self.nric is not None):
            print(f"Welcome {self.name}!")
            print("1. Single check in")
            print("2. Single check out")
            print("3. Group check in")
            print("4. Group check out")
            print("5. List history")
            print("6. Declare covid notification(MOH Officer)")
            print("7. Logout")
            if utils.mode == 1: 
                print("8. Load json file")

            userChoice = int(input("Select an option:"))

            if userChoice == 1:
                self.SingleCheckIn()
            elif userChoice == 2:
                self.SingleCheckOut()
            elif userChoice == 3:
                self.GroupCheckIn()
            elif userChoice == 4:
                self.GroupCheckOut()
            elif userChoice == 5:
                self.ListHistory()
            elif userChoice == 6:
                self.NotifyCovidCase()
            elif userChoice == 7:
                self.Logout()
            elif userChoice == 8:
                self.LoadJSONFile()
        else:
            pass
    
if __name__ == '__main__':
    # mode is 1 for testing purposes
    utils.mode = 1

    nric = None
    while nric is None:
        nric = input("Enter your NRIC: ")

    client = Client(nric)
    while True:
        client.Run()