from sqlalchemy import Column, String, Text, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref, declarative_base

Base = declarative_base()


class Gym(Base):
    __tablename__ = 'gym_app_gym'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    address_city = Column(String(255), nullable=False)
    address_street = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Gym(name={self.name})>"


class Machine(Base):
    __tablename__ = 'gym_app_machine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    type = Column(String(100), nullable=False)
    model = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False)
    maintenance_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<Machine(type={self.type}, serial_number={self.serial_number})>"


class HallType(Base):
    __tablename__ = 'gym_app_hall_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), unique=True, nullable=False)
    type_description = Column(Text, nullable=False)

    def __repr__(self):
        return f"<HallType(name={self.name})>"

    def save(self, session):
        self.code = self.code.upper()
        session.add(self)
        session.commit()


class Hall(Base):
    __tablename__ = 'gym_app_hall'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    users_capacity = Column(Integer, default=10, nullable=False)
    hall_type_id = Column(Integer, ForeignKey('hall_type.id'), nullable=False)
    gym_id = Column(Integer, ForeignKey('gym.id'), nullable=False)

    hall_type = relationship("HallType", backref=backref("halls", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<Hall(name={self.name})>"


class Admin(Base):
    __tablename__ = 'gym_app_admin'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    gym_id = Column(Integer, ForeignKey('gym.id'), nullable=False)
    address_city = Column(String(255), nullable=False)
    address_street = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Admin(name={self.name})>"


class Employee(Base):
    __tablename__ = 'gym_app_employee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    gym_id = Column(Integer, ForeignKey('gym.id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('employee.id'), nullable=True)
    address_city = Column(String(255), nullable=False)
    address_street = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    positions = Column(Text, nullable=True, default="")

    manager = relationship("Employee", remote_side="Employee.id", backref=backref("subordinates", cascade="all"))

    def __repr__(self):
        return f"<Employee(name={self.name})>"

    @hybrid_property
    def position_list(self):
        return [pos.strip() for pos in self.positions.split(",") if pos.strip()]

    @position_list.setter
    def position_list(self, position_list):
        self.positions = ", ".join(position_list)


class Member(Base):
    __tablename__ = 'gym_app_member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gym_id = Column(Integer, ForeignKey('gym.id'), nullable=False)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    phone_number = Column(String(20), nullable=True, unique=True)


    def __repr__(self):
        return f"<Member(name={self.name})>"


class HallMachine(Base):
    __tablename__ = 'gym_app_hall_machine'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hall_id = Column(Integer, ForeignKey('hall.id'), nullable=False)
    machine_id = Column(Integer, ForeignKey('machine.id'), nullable=False)
    name = Column(String(255), nullable=True)
    uid = Column(String(100), unique=True, nullable=False)

    hall = relationship("Hall", backref=backref("hall_machines", cascade="all, delete-orphan"))
    machine = relationship("Machine", backref=backref("hall_machines", cascade="all, delete-orphan"))

    __table_args__ = (UniqueConstraint('hall_id', 'machine_id', name='_hall_machine_uc'),)

    def __repr__(self):
        return f"<HallMachine(machine={self.machine}, hall={self.hall})>"

    def save(self, session):
        if not self.uid:
            existing = session.query(HallMachine).filter_by(hall_id=self.hall_id, machine_id=self.machine_id).first()
            if existing:
                return
            count = session.query(HallMachine).filter_by(hall_id=self.hall_id, machine_id=self.machine_id).count() + 1
            self.uid = f"{self.machine.type}_{count}"

            while session.query(HallMachine).filter_by(uid=self.uid).first():
                count += 1
                self.uid = f"{self.machine.type}_{count}"

        session.add(self)
        session.commit()
