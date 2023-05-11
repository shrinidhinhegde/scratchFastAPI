from sqlalchemy import Column, String, Integer, Sequence, text

from src.database import Base


class Student(Base):
    __tablename__ = 'student'

    seq = Sequence('student_id_seq', metadata=Base.metadata, start=1001, increment=2, minvalue=1001)

    id = Column(Integer, seq, primary_key=True, index=True, server_default=seq.next_value())
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)


class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, index=True, server_default=text("currval('student_id_seq'::regclass)"))
    name = Column(String(50), nullable=False)
    total_students = Column(Integer, nullable=False, default=0)
