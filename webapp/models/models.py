from sqlalchemy import Column, String, Integer, Date, REAL, Text
from webapp.database import Base, db_session, init_db

class ContentClassificationTask(Base):
    __tablename__ = 'content_classification_tasktable'

    __table_args__ = {'extend_existing': True}

    index = Column(Integer, primary_key=True)
    object_id = Column(String(255))
    task_status = Column(String(64))
    n_failed = Column(Integer, default=0)
    max_retries = Column(Integer, default=0)
    max_timeout = Column(REAL())
    priority_factor = Column(REAL())
    updated_at = Column(REAL())
    created_at = Column(REAL())
    last_submitted = Column(REAL())
    last_queried = Column(REAL())
    last_success = Column(REAL())
    last_failure = Column(REAL())
    endpoint = Column(Text)
    params = Column(Text) # jason
    task_id = Column(String(132))
    state = Column(String(64))
    res_status = Column(String(64))
    res_data = Column(Text) # jason
    res_error = Column(Text) # jason
    f_no_total_clicks = Column(Integer, default=0)
    f_no_unique_clicks = Column(Integer, default=0)
    _uuid = Column(String(132))

    def __init__(self, **kwargs):
        self._uuid = kwargs['_uuid']
        self.index = kwargs['index']

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def saveOne(self):
        db_session.add(self)

        db_session.commit()
        db_session.close()

    @classmethod
    def saveAll(cls, dataList):
        for d in dataList:
            cck = cls(**d)
            db_session.add(cck)

        db_session.commit()
        db_session.close()

if __name__ == '__main__':
    data = {
        '_uuid': 'xxxxxx',
        'index': 99999
    }
    cck = ContentClassificationTask(**data)

    cck.saveOne()

#     data = [
#         {'status': 'Rain', 'xxx': 'test'},
#         {'status': 'Storm', 'xxx': 'test2'},
#     ]
#
#     ContentClassificationTask.saveAll(data)
