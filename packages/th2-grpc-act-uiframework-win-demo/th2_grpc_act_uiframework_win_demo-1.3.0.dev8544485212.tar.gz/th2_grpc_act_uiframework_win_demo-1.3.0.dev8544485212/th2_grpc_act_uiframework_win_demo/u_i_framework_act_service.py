from . import uiframework_win_demo_pb2_grpc as importStub

class UIFrameworkActService(object):

    def __init__(self, router):
        self.connector = router.get_connection(UIFrameworkActService, importStub.UIFrameworkActStub)

    def register(self, request, timeout=None, properties=None):
        return self.connector.create_request('register', request, timeout, properties)

    def unregister(self, request, timeout=None, properties=None):
        return self.connector.create_request('unregister', request, timeout, properties)

    def openApplication(self, request, timeout=None, properties=None):
        return self.connector.create_request('openApplication', request, timeout, properties)

    def closeApplication(self, request, timeout=None, properties=None):
        return self.connector.create_request('closeApplication', request, timeout, properties)

    def initConnection(self, request, timeout=None, properties=None):
        return self.connector.create_request('initConnection', request, timeout, properties)

    def closeConnection(self, request, timeout=None, properties=None):
        return self.connector.create_request('closeConnection', request, timeout, properties)

    def sendNewOrderSingle(self, request, timeout=None, properties=None):
        return self.connector.create_request('sendNewOrderSingle', request, timeout, properties)

    def extractLastOrderDetails(self, request, timeout=None, properties=None):
        return self.connector.create_request('extractLastOrderDetails', request, timeout, properties)

    def extractLastSystemMessage(self, request, timeout=None, properties=None):
        return self.connector.create_request('extractLastSystemMessage', request, timeout, properties)