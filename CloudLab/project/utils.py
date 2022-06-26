from queue import Queue

# mode 0 = normal, mode 1 = testing
mode = 0

# formatting of date and time
format_date = "%d/%m/%Y"
format_time = "%I:%M%p"
format_datetime = "%d/%m/%Y %I:%M%p"

# load filename of json
filename = "records.json"

notificationMessage = '''
You have visited the location ({}) on the same 
day as several other COVID-19 positive cases on 
{} between {} and {}.
You are strongly encouraged to minimise all social 
interactions until {}. Please monitor your health
and seek medical attention if unwell.
'''

# A client helper class to add/remove client NRIC and notification messages
class ClientSingleton(object):
    _instance = None
    # dictionary to store client notifications in a Queue
    _notificationQ = {}
    # list to store client NRIC
    _clientIDList = []

    # Creating object singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ClientSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # Create a notification queue data structure for the client and add NRIC to client list
    def addClient(self, nric, context):
        self._notificationQ[nric] = Queue()
        self._clientIDList.append(nric)
    
    # Remove notification queue data structure for the client and remove NRIC from client list
    def removeClient(self, nric):
        self._notificationQ.pop(nric)
        self._clientIDList.remove(nric)
    
    # Add notification message in the queue for the client
    def addNotificationQ(self, nric, info):
        if nric in self._clientIDList:
            self._notificationQ[nric].put(info)
    
    # Remove notification message in the queue for the client
    def getNotification(self, nric):
        return self._notificationQ[nric].get()
    
    # Check if client NRIC is available in the list
    def isNRICAvailable(self, nric):
        return nric in self._clientIDList
    
    # Return clients' NRIC list
    def getClientIDList(self):
        return self._clientIDList