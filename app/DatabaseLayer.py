__author__ = 'zexxonn'

from app import db
from models import ServerStateInfo
from models import UserMessage
from ServerStates import ServerStateId
from ServerStates import MessageTypeId
from datetime import datetime

class DatabaseLayer(object):

    @staticmethod
    def getServerState(userId):
        query = db.session.query(ServerStateInfo.stateType).\
                                                    filter(ServerStateInfo.userId == userId)
        res = query.all()
        if res:
            return res[0][0]

        baseState = ServerStateId(ServerStateId.SERVER_BASE_STATE)
        ssi = ServerStateInfo(userId=userId, eventTime=datetime.now(),
                              stateType=str(baseState), description="")
        db.session.add(ssi)
        db.session.commit()

        return baseState.value

    @staticmethod
    def updateServerState(userId, serverStateId):

        try:
            ServerStateInfo.query.filter_by(userId = userId).update(dict(stateType = str(serverStateId)))
            db.session.commit()
        except Exception as ex:
            ssi = ServerStateInfo(userId=userId, eventTime=datetime.now(),
                                  stateType=str(serverStateId), description="")
            db.session.add(ssi)
            db.session.commit()

    @staticmethod
    def saveLocation(userId, latitude, longitude):
        DatabaseLayer.saveUserMessage(userId,
                                      "lat={} long={}".format(latitude, longitude),
                                      MessageTypeId(MessageTypeId.LOCATION_INFO))

    @staticmethod
    def saveCurrencyPairRequest(userId, message):
        DatabaseLayer.saveUserMessage(userId,message, MessageTypeId(MessageTypeId.CCY_PAIR_REQUEST))

    @staticmethod
    def saveSimpleMessage(userId, message):
        DatabaseLayer.saveUserMessage(userId,message, MessageTypeId(MessageTypeId.SIMPLE_MESSAGE))

    @staticmethod
    def saveUserMessage(userId, message, messageType):
        um = UserMessage(userId=userId, eventTime=datetime.now(), message=message, messageType=str(messageType))
        db.session.add(um)
        db.session.commit()
