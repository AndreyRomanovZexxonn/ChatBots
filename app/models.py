__author__ = 'zexxonn'

from app import db
from ServerStates import ServerStateId
from ServerStates import MessageTypeId

class ServerStateInfo(db.Model):
    userId = db.Column(db.BigInteger, primary_key=True, index=True)
    eventTime = db.Column(db.DateTime)
    stateType = db.Column(db.String(100), default=str(ServerStateId.SERVER_BASE_STATE))
    description = db.Column(db.String(100))

    def __repr__(self):
        return '[{}, {}, {}, {}]'.format(self.userId, self.eventTime, self.stateType, self.description)


class UserMessage(db.Model):
    userId = db.Column(db.BigInteger, db.ForeignKey(ServerStateInfo.userId), primary_key=True, index=True)
    eventTime = db.Column(db.DateTime, primary_key=True)
    message = db.Column(db.String(200), default=ServerStateId(ServerStateId.SERVER_BASE_STATE))
    messageType = db.Column(db.String(100), default=MessageTypeId(MessageTypeId.SIMPLE_MESSAGE))

    def __repr__(self):
        return '[{}, {}, {}, {}]'.format(self.userId, self.eventTime, self.message, self.messageType)
