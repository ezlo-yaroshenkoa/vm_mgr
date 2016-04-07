from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class vm(Base):
    __tablename__ = 'vm'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True)

class vms_db(object):
    def __init__(self):
        self.engine_ = create_engine('sqlite:///vms.db')
        self.session_maker_ = sessionmaker()
        self.session_maker_.configure(bind=self.engine_)
        Base.metadata.create_all(self.engine_)

    def add(self, vm_name):
        session = self.session_maker_()
        if not session.query(session.query(vm).filter_by(name=vm_name).exists()).scalar():
            v = vm(name=vm_name)
            session.add(v)
            session.commit()

    def delete(self, vm_name):
        session = self.session_maker_()
        session.query(vm).filter_by(name=vm_name).delete(synchronize_session=False)
        session.commit()

    def get_all(self):
        result = []

        session = self.session_maker_()
        vms =  session.query(vm).all()
        for v in vms:
            result.append(v.name)

        return result