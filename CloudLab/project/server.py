from concurrent import futures

import logging

from concurrent import futures

import grpc
import safe_entry_pb2 as se_pb2
import safe_entry_pb2_grpc as se_pb2_grpc

import json
import datetime as dt
import utils as utils

# A class for handling Safe Entry service
class SafeEntry(se_pb2_grpc.SafeEntryServicer):
    # Initialisation
    def __init__(self):
        super().__init__()
        # create a client helper class singleton
        self.clients = utils.ClientSingleton()

    # Login to the server
    def Login(self, request, context):
        # check if nric has already login
        if request.nric in self.clients.getClientIDList():
            return se_pb2.LoginResponse(status=se_pb2.Status.ERROR)

        self.clients.addClient(request.nric, context)
        print("List of clients: ", self.clients.getClientIDList())

        name = None
        with open(utils.filename, "r+") as file:
            data = json.load(file)
            name = data["user_details"][request.nric]
            
        return se_pb2.LoginResponse(status=se_pb2.Status.SUCCESS, name=name)

    # Logout of the server
    def Logout(self, request, context):
        self.clients.removeClient(request.nric)
        print("List of clients: ", self.clients.getClientIDList())
            
        return se_pb2.LoginResponse(status=se_pb2.Status.SUCCESS)

    # Check if user has notification message(s) for possible exposure of covid
    def NotificationCheck(self, request, context):
        arr = []
        
        with open(utils.filename, "r+") as file:
            data = json.load(file)
            # check though the user's safeEntry records for the dates that were recorded for possible exposure to covid
            if request.nric in data["user_history"]:
                for history in data["user_history"][request.nric]:
                    if "exposure" in history:
                        # calculate the past 14 days date
                        currDate = dt.datetime.now().date()
                        past14Days = currDate - dt.timedelta(days=14)
                        # convert date formatting for the user date of visit
                        recDate = dt.datetime.strptime(history["date"], utils.format_date).date()

                        # only if the user were at the place of possible exposure within past 14 days then send them notification message(s)
                        if recDate >= past14Days:
                            arr.append(utils.notificationMessage.format(
                                            history["location"], history["date"],
                                            history["checkin_time"], history["checkout_time"],
                                            history["end_date"]
                                        ))

        return se_pb2.NotificationListResponse(message=arr)
    
    # User's open stream to check for live notifications from a separate thread
    def SubscribeNotification(self, request, context):
        # while there is notification message in the user's queue, send out the notification message to the user
        while self.clients.isNRICAvailable(request.nric):
            yield se_pb2.NotificationResponse(message=self.clients.getNotification(request.nric))

    # Check user's latest SafeEntry record check in/out status
    def CheckForStatus(self, request, context):
         with open(utils.filename, "r") as file:
            data = json.load(file)

            if request.nric in data["user_history"]:
                # check if latest record from user's history has been already checked out
                if data["user_history"][request.nric][-1]["checkout_time"] == "":
                    if "group" in data["user_history"][request.nric][-1]:
                        return se_pb2.CheckResponse(status=se_pb2.Status.GFAILURE)
                    else:
                        return se_pb2.CheckResponse(status=se_pb2.Status.SFAILURE)

            return se_pb2.CheckResponse(status=se_pb2.Status.SUCCESS)

    # Check for groups' latest SafeEntry record check in statuses
    def CheckForGroupStatus(self, request, context):
        with open(utils.filename, "r") as file:
            data = json.load(file)
            arr = []

            # loop through the list of nric and check if any of the user has already been checked out
            for req in request.nric:
                if req.nric in data["user_history"]:
                    if data["user_history"][req.nric][-1]["checkout_time"] == "":
                        arr.append(se_pb2.NRIC(nric=req.nric))
 
            if arr:
                return se_pb2.GroupCheckResponse(status=se_pb2.Status.FAILURE,nric=arr)
                            
            return se_pb2.GroupCheckResponse(status=se_pb2.Status.SUCCESS)

    # Single check in
    def SingleCheckIn(self, request, context):
        with open(utils.filename, "r+") as file:
            data = json.load(file)

            # record the date, time and location of the check in
            new_data = {"date":request.date, "location":request.location, 
            "checkin_time":request.checkin_time, "checkout_time":""}

            if request.user.nric not in data["user_history"]:
                data["user_history"][request.user.nric] = []
            data["user_history"][request.user.nric].append(new_data)

            file.seek(0)
            json.dump(data, file, indent = 4)

        return se_pb2.CheckResponse(status=se_pb2.Status.SUCCESS)

    # Single check out
    def SingleCheckOut(self, request, context):
        with open(utils.filename, "r+") as file:
            data = json.load(file)
            # record the time of check out
            data["user_history"][request.user.nric][-1]["checkout_time"] = request.checkout_time
            file.seek(0)
            json.dump(data, file, indent = 4)

        return se_pb2.CheckResponse(status=se_pb2.Status.SUCCESS)
    
    # Group check in
    def GroupCheckIn(self, request, context):
        arr = []
        with open(utils.filename, "r+") as file:
            data = json.load(file)

            # store all the affected users' NRIC
            for id in request.nric:
                arr.append(id.nric)

            # record the date, time and location of the check in for all the affected users
            for user in request.checkRequest:     
                new_data = {"date":user.date, "location":user.location, 
                "checkin_time":user.checkin_time, "checkout_time":"", "group": True, 
                "grouping": arr}
                if user.user.nric not in data["user_history"]:
                    data["user_history"][user.user.nric] = []
                data["user_history"][user.user.nric].append(new_data)

            file.seek(0)
            json.dump(data, file, indent = 4)

        return se_pb2.CheckResponse(status=se_pb2.Status.SUCCESS)
    
    # Group check out
    def GroupCheckOut(self, request, context):
        with open(utils.filename, "r+") as file:
            data = json.load(file)
            # record the time of check out for all the affected users
            for nric in data["user_history"][request.user.nric][-1]["grouping"]:
                data["user_history"][nric][-1]["checkout_time"] = request.checkout_time
            file.seek(0)
            json.dump(data, file, indent = 4)
        return se_pb2.CheckResponse(status=se_pb2.Status.SUCCESS)

    # List user's history date, location and check in/out time
    def ListHistory(self, request, context):
        arr = []
        with open(utils.filename, "r") as file:
            data = json.load(file)
  
        # check if user's NRIC is within the json file, then sent back to client their history information
        if request.nric in data["user_history"]:
            for msg in data["user_history"][request.nric]:
                arr.append(se_pb2.HistoryResponse(date=msg["date"],
                location=msg["location"],
                checkin_time=msg["checkin_time"],
                checkout_time=msg["checkout_time"]))
            return se_pb2.HistoryListResponse(historyListResponse=arr)
        else:
            return se_pb2.HistoryListResponse(historyListResponse=arr)  
    
    # Special remote access
    # MOH officers able to declare location has been visited by a COVID-19 case.
    # Able to set the date, time and location of exposure of covid case.
    # This function will able record and sent a notification to possible affected users
    # based on SafeEntry records
    def NotifyCovidCase(self, request, context):
        # convert date and time formatting for the declaration date
        visitDate = "{} {}".format(request.date, request.time)
        visitDate = dt.datetime.strptime(visitDate, utils.format_datetime)
        
        # calculate the end date <D14> for possible exposure to covid
        endDate = visitDate.date() + dt.timedelta(days=14)
        endDate = endDate.strftime(utils.format_date)
        
        # calculate the past 14 days date
        currDate = dt.datetime.now().date()
        past14Days = currDate - dt.timedelta(days=14)

        with open(utils.filename, "r+") as file:
            data = json.load(file)
            # record the date, time and location of the covid exposure declaration
            new_data = {"date":request.date, "location":request.location ,"time":request.time}
            data["covid_history"].append(new_data)
          
            # check through SafeEntry records 
            for user in data["user_history"]:
                for history in data["user_history"][user]:
                    if(history["location"] == request.location):
                        # convert date and time formatting for the user check in
                        checkin_str = "{} {}".format(history["date"], history["checkin_time"])
                        checkin = dt.datetime.strptime(checkin_str, utils.format_datetime)
                        
                        # convert date formatting for the user date of visit
                        recDate = dt.datetime.strptime(history["date"], utils.format_date).date()

                        if history["checkout_time"] != "":
                            # convert date and time formatting for the user check out
                            checkout_str = "{} {}".format(history["date"], history["checkout_time"])
                            checkout = dt.datetime.strptime(checkout_str, utils.format_datetime)

                            # check if declaration date is within the user's check in and out date
                            if visitDate >= checkin and visitDate <= checkout:
                                history["exposure"] = True
                                history["end_date"] = endDate
                                
                                # only if the user were at the place of possible exposure within past 14 days then send them notification message(s)
                                if recDate >= past14Days:
                                    self.clients.addNotificationQ(str(user),
                                    utils.notificationMessage.format(
                                        history["location"], history["date"],
                                        history["checkin_time"], history["checkout_time"],
                                        history["end_date"]
                                    ))
                                
                        else:
                            # check if declaration date is more than the user's check in date (this is assuming that user is considered not checked out)
                            if visitDate >= checkin:
                                history["exposure"] = True
                                history["end_date"] = endDate
                                
                                # only if the user were at the place within past 14 days then send them notification
                                if recDate >= past14Days:
                                    self.clients.addNotificationQ(str(user),
                                    utils.notificationMessage.format(
                                        history["location"], history["date"],
                                        history["checkin_time"], history["checkout_time"],
                                        history["end_date"]
                                    ))
                                    
            file.seek(0)
            json.dump(data, file, indent = 4)
                           
        return se_pb2.Empty()

    def LoadJSONFile(self, request, context):
        utils.filename = request.filename + ".json"
        print("Loaded {} file successfully...".format(utils.filename))

        return se_pb2.CheckResponse(status=se_pb2.Status.SUCCESS)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    se_pb2_grpc.add_SafeEntryServicer_to_server(SafeEntry(), server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    print("starting gRPC server...")
    logging.basicConfig()
    serve()