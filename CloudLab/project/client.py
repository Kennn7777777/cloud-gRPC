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

class Client(object):
    def __init__(self, nric):
        self.nric = nric

        # create a gRPC channel to connect to server
        self.channel = grpc.insecure_channel('localhost:50051')
        # create a gRPC stub to communicate to server
        self.stub = se_pb2_grpc.SafeEntryStub(self.channel)

        # login to server
        response = self.stub.Login(se_pb2.LoginRequest(nric=nric))
        if response:
            if response.status == se_pb2.Status.SUCCESS:
                print("Login successfully!\n")
            else:
                print("Login fail...\n")
        else:
            print("Some error has occur...\n")
    
        # check if user has notification message(s) for possible exposure of covid and print them
        response = self.stub.NotificationCheck(se_pb2.NRIC(nric=self.nric))
        for msg in response.message:
            print(msg) 

        # create a thread to listen for new incoming notification message(s) stream
        threading.Thread(target=self.__listen_for_notifications, daemon=True).start()

    def __listen_for_notifications(self):
        # listen for incoming notification message(s) stream
        for noti in self.stub.SubscribeNotification(se_pb2.NRIC(nric=self.nric)):
            print(noti.message)
        
    def SingleCheckIn(self):
        # check if user has not check out from previous (single/group) location
        request = se_pb2.NRIC(nric=self.nric)
        response = self.stub.CheckForStatus(request)

        # if previous location was already check out, do a new check in for new location
        if response.status == se_pb2.Status.SUCCESS:
            name = input("Enter name: ")
            location = input("Enter location: ")

            # convert date and time formatting
            date = dt.datetime.now().strftime(utils.format_date)
            checkin_time = dt.datetime.now().strftime(utils.format_time)
            #date = input("Enter date: ")
            #checkin_time = input("Enter checkin time: ")
            
            # send request for single check in
            request1 = se_pb2.CheckRequest(user=se_pb2.User(name=name,nric=self.nric),
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

    def SingleCheckOut(self):
        # check if user has not check in from previous (single/group) location
        request = se_pb2.NRIC(nric=self.nric)
        response = self.stub.CheckForStatus(request)

        # if previous location was not check out yet for Single
        if response.status == se_pb2.Status.SFAILURE:
            #checkout_time = input("Enter checkout time: ")
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
     
    def GroupCheckIn(self):
        arr = []
        nricList = []
        count = 0
        # do not allow the user to type negative or 1 number
        while count <= 1:
            count = int(input("Enter how many members(including youself >1): "))
        
        # convert date and time formatting
        date = dt.datetime.now().strftime(utils.format_date)
        checkin_time = dt.datetime.now().strftime(utils.format_time)
        # checkin_time = input("Enter checkin time: ")
        # date = input("Enter date: ")
        location = input("Enter location: ")

        # loop through the number of family members for their name and NRIC
        # person 1 should be yourself
        for i in range(count):
            name = input(f"Enter name for person {i+1}: ")
            nric = input(f"Enter NRIC for person {i+1}: ")         
            arr.append(se_pb2.CheckRequest(user=se_pb2.User(name=name,nric=nric),
            date=date,
            location=location,
            checkin_time=checkin_time))
            nricList.append(se_pb2.NRIC(nric=nric))
        
        request = se_pb2.NRICList(nric=nricList)
        response = self.stub.CheckForGroupStatus(request)

        if response.status == se_pb2.Status.SUCCESS:
            # send request for group check in
            response1 = self.stub.GroupCheckIn(se_pb2.GroupCheckRequest(checkRequest=arr,nric=nricList))
            if response1.status == se_pb2.Status.SUCCESS:
                print("Group Check in successfully!\n")
            else:
                print("Group Check in unsuccessful...\n")
        elif response.status == se_pb2.Status.FAILURE:
            converted_list = [str(element.nric) for element in response.nric]
            nric_list = ",".join(converted_list)
    
            print("Group Check in unsuccessful...NRIC {} to check out for previous location first!\n".format(nric_list))
        else:
            print("Some error has occur...Please try again...\n")
 
    def GroupCheckOut(self):
        # check if user has not check in from previous (single/group) location
        request = se_pb2.NRIC(nric=self.nric)
        response = self.stub.CheckForStatus(request)

        # if previous location was not check out yet for Group
        if response.status == se_pb2.Status.GFAILURE:
            #checkout_time = input("Enter checkout time: ")
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
            print("Group Check out unsuccessful...You have not check in any location yet....")
        else:
            print("Some error has occur...Please try again...\n")

    def Logout(self):
        # logout from server and exit client
        response = self.stub.Logout(se_pb2.LoginRequest(nric=self.nric))

        if response:
            if response.status == se_pb2.Status.SUCCESS:
                print("Logout successfully!\n")
            else:
                print("Logout failed...\n")
        else:
            print("Some error has occur...\n")
        
        sys.exit()

    def Run(self):
        if (self.nric is not None):
            print("1. Single check in")
            print("2. Single check out")
            print("3. Group check in")
            print("4. Group check out")
            print("5. List history")
            print("6. Declare covid notification(MOH Officer)")
            print("7. Logout")

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
                request = se_pb2.HistoryRequest(nric=self.nric)
                print("+-------------------------------------------------------------------+")
                print("|-----------------------------History List--------------------------|")
                print("+----------------+----------------+----------------+----------------+")
                print("|Date            |location        |checkin time    |checkout time   |")
                print("+----------------+----------------+----------------+----------------+")
                response = self.stub.ListHistory(request)
                space = ' '
                max_space = 16
                if not response.historyListResponse:
                     print("|                        No records Found!                          |")

                for resp in response.historyListResponse:
                    print(f"|{resp.date}{abs(max_space-len(resp.date))*space}|{resp.location}{abs(max_space-len(resp.location))*space}|{resp.checkin_time}{abs(max_space-len(resp.checkin_time))*space}|{resp.checkout_time}{abs(max_space-len(resp.checkout_time))*space}|")
                
                print("+----------------+----------------+----------------+----------------+\n")
            elif userChoice == 6:
                date = input("Enter date(DD/MM/YYYY): ")
                time = input("Enter time(HH:MM(AM/PM)): ")
                location = input("Enter location: ")
                
                self.stub.NotifyCovidCase(se_pb2.NotificationRequest(date=date, time=time, location=location))
            elif userChoice == 7:
                self.Logout()
        else:
            pass
    
if __name__ == '__main__':
    #logging.basicConfig()
    # run()
    nric = None
    while nric is None:
        nric = input("Enter your NRIC: ")

    client = Client(nric)
    while True:
        client.Run()