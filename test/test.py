from app import db, models
from datetime import datetime

#query = db.session.query(models.ServerStateInfo.stateType).filter(models.ServerStateInfo.userId == 1123)


query = models.ServerStateInfo.query.filter_by(userId = 1458021930921355).update(dict(description = 'my_new_email@example.com'))


res = query.first()
print(res)

users = models.ServerStateInfo.query.all()
for u in users:
    print(u)

