import sqlalchemy # type: ignore
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, Text, Date # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash

Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = 'gym_app_user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)

    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str):
        return self.hashed_password ==  generate_password_hash(password)

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
    user_id = Column(Integer, ForeignKey('gym_app_user.id'), nullable=False)

    gym = relationship("Gym", back_populates="admins")
    user = relationship("User")


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
    user_id = Column(Integer, ForeignKey('gym_app_user.id'), nullable=False)

    gym = relationship("Gym", back_populates="employees")
    manager = relationship('Employee', remote_side=[id])
    user = relationship("User")


class Member(Base):
    __tablename__ = 'gym_app_member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gym_id = Column(Integer, ForeignKey('gym_app_gym.id'), nullable=False)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey('gym_app_user.id'), nullable=False)

    gym = relationship("Gym", back_populates="members")
    user = relationship("User")

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
        return (f"<HallMachine(id={self.id}, hall_id={self.hall_id}, machine_id={self.machine_id},"
                f" name={self.name}, uid={self.uid})>")
