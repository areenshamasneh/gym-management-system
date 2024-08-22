from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, Text, Date
from sqlalchemy.event import listens_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from gym_management.settings import SessionLocal

Base = declarative_base()


class Gym(Base):
    __tablename__ = 'gym_app_gym'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    address_city = Column(String(255), nullable=False)
    address_street = Column(String(255), nullable=False)

    halls = relationship("Hall", back_populates="gym")
    admins = relationship("Admin", back_populates="gym")
    employees = relationship("Employee", back_populates="gym")
    members = relationship("Member", back_populates="gym")


class Machine(Base):
    __tablename__ = 'gym_app_machine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    type = Column(String(100), nullable=False)
    model = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False)
    maintenance_date = Column(Date, nullable=True)

    hall_machines = relationship("HallMachine", back_populates="machine")


class HallType(Base):
    __tablename__ = 'gym_app_halltype'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), unique=True, nullable=False)
    type_description = Column(Text, nullable=False)

    halls = relationship("Hall", back_populates="hall_type")

    def save(self):
        self.code = self.code.upper()


class Hall(Base):
    __tablename__ = 'gym_app_hall'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    users_capacity = Column(Integer, default=10)
    hall_type_id = Column(Integer, ForeignKey('gym_app_halltype.id'), nullable=False)
    gym_id = Column(Integer, ForeignKey('gym_app_gym.id'), nullable=False)

    hall_type = relationship("HallType", back_populates="halls")
    gym = relationship("Gym", back_populates="halls")
    hall_machines = relationship("HallMachine", back_populates="hall")


class Admin(Base):
    __tablename__ = 'gym_app_admin'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    gym_id = Column(Integer, ForeignKey('gym_app_gym.id'), nullable=False)
    address_city = Column(String(255), nullable=False)
    address_street = Column(String(255), nullable=False)

    gym = relationship("Gym", back_populates="admins")


class Employee(Base):
    __tablename__ = 'gym_app_employee'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String(20), default="")
    email = Column(String(254), nullable=False, unique=True)
    address_city = Column(String(255), nullable=False)
    address_street = Column(String(255), nullable=False)
    positions = Column(String, nullable=False)
    gym_id = Column(Integer, ForeignKey('gym_app_gym.id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('gym_app_employee.id'), nullable=True)

    gym = relationship("Gym", back_populates="employees")
    manager = relationship('Employee', remote_side=[id], backref='subordinates')


class Member(Base):
    __tablename__ = 'gym_app_member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gym_id = Column(Integer, ForeignKey('gym_app_gym.id'), nullable=False)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=True)

    gym = relationship("Gym", back_populates="members")


class HallMachine(Base):
    __tablename__ = 'gym_app_hallmachine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hall_id = Column(Integer, ForeignKey('gym_app_hall.id'), nullable=False)
    machine_id = Column(Integer, ForeignKey('gym_app_machine.id'), nullable=False)
    name = Column(String(255), nullable=True)
    uid = Column(String(100), unique=True, nullable=False)

    hall = relationship("Hall", back_populates="hall_machines")
    machine = relationship("Machine", back_populates="hall_machines")

    __table_args__ = (UniqueConstraint('hall_id', 'machine_id', name='_hall_machine_uc'),)

    def __repr__(self):
        return f"<HallMachine(id={self.id}, hall_id={self.hall_id}, machine_id={self.machine_id}, name={self.name}, uid={self.uid})>"


def generate_uid(session, hall_id, machine_id):
    count = session.query(HallMachine).filter_by(hall_id=hall_id, machine_id=machine_id).count() + 1
    return f"{machine_id}_{count}"


@listens_for(HallMachine, 'before_insert')
def before_insert(mapper, connection, target):
    session = SessionLocal()
    try:
        if not target.uid:
            existing = session.query(HallMachine).filter_by(hall_id=target.hall_id,
                                                            machine_id=target.machine_id).first()
            if not existing:
                target.uid = generate_uid(session, target.hall_id, target.machine_id)
            while session.query(HallMachine).filter_by(uid=target.uid).first():
                target.uid = generate_uid(session, target.hall_id, target.machine_id)
    except IntegrityError:
        session.rollback()
    finally:
        session.close()
