import inspect
from sqlalchemy import Column, ForeignKey, Integer, Table, VARCHAR
from sqlalchemy.orm import relationship


def get_classes(db, names=None):
    """
    Return a sqlalchemy model classes.

    :param db: sqlalchemy database object
    :param names: must be None, str or List of Strings, Defines the needed classses, which shall be returned.
    :return: duct of classes, if names is None or List of given class names. single class, if name is a String.
    """

    Base = db.Base
    metadata = Base.metadata

    class Employee(Base):
        __tablename__ = 'Employee'
        emp_id = Column(Integer, primary_key=True)
        name = Column(VARCHAR(length=30), nullable=False)
        authorization = Column(VARCHAR(length=5), nullable=False)
        grade = Column(VARCHAR(length=5), nullable=False)
        emp_rel = relationship('CompetencyHub', backref="emp")

        def __init__(self, emp_id, name, authorization, grade):
            self.emp_id = emp_id
            self.name = name
            self.authorization = authorization
            self.grade = grade

    class EmployeeManager(Base):
        __tablename__ = 'EmployeeManager'
        emp_id = Column(ForeignKey('Employee.emp_id'), primary_key=True, nullable=False)
        man_id = Column(ForeignKey('Employee.emp_id'), nullable=False)

        def __init__(self, emp_id, man_id):
            self.emp_id = emp_id
            self.man_id = man_id

    class Access(Base):
        __tablename__ = 'Access'

        emp_id = Column(ForeignKey('Employee.emp_id'), primary_key=True, nullable=False)
        password = Column(VARCHAR, nullable=False)
        employee = relationship('Employee')

        def __init__(self, emp_id, password):
            self.password = password
            self.emp_id = emp_id

    class levels(Base):
        __tablename__ = "levels"

        id = Column(Integer, primary_key=True, nullable=False)
        val = Column(VARCHAR(length=5), nullable=False)
        rdct_rel = relationship('CompetencyHub', backref="lvl")

        def __init__(self, val, id):
            self.val = val
            self.id = id

    class Offering(Base):
        __tablename__ = "Offering"

        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        text = Column(VARCHAR(length=255), nullable=False)
        offer_rel = relationship('CompetencyHub', backref="offer")

        def __int__(self, id, text):
            self.id = id
            self.text = text

    class Technology(Base):
        __tablename__ = "Technology"

        id = Column(Integer, primary_key=True, nullable=False)
        tech = Column(VARCHAR(length=20), nullable=False)
        tech_rel = relationship('CompetencyHub', backref="tech")

        def __init__(self, id, tech):
            self.id = id
            self.tech = tech

    class Microcontroller(Base):
        __tablename__ = "Microcontroller"

        id = Column(Integer, primary_key=True, nullable=False)
        text = Column(VARCHAR(length=20), nullable=False)
        micro_rel = relationship('CompetencyHub', backref="micro")

        def __int__(self, id, text):
            self.id = id
            self.text = text

    class Tools(Base):
        __tablename__ = "Tools"

        id = Column(Integer, primary_key=True, nullable=False)
        text = Column(VARCHAR(length=20), nullable=False)
        tools_rel = relationship('CompetencyHub', backref="tools")

        def __int__(self, id, text):
            self.id = id
            self.text = text

    class Company(Base):
        __tablename__ = "Company"

        id = Column(Integer, primary_key=True, nullable=False)
        text = Column(VARCHAR(length=20), nullable=False)
        comp_rel = relationship('CompetencyHub', backref="company")

        def __int__(self, id, text):
            self.id = id
            self.text = text

    class Ps1(Base):
        __tablename__ = "Ps1"

        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        text = Column(VARCHAR(length=20), nullable=True)
        ps1_rel = relationship('CompetencyHub', backref="ps1")

        def __int__(self, id, text):
            self.id = id
            self.text = text

    class Ps2(Base):
        __tablename__ = "Ps2"

        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        text = Column(VARCHAR(length=20), nullable=True)
        ps2_rel = relationship('CompetencyHub', backref="ps2")

        def __int__(self, id, text):
            self.id = id
            self.text = text

    class Ps3(Base):
        __tablename__ = "Ps3"

        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        text = Column(VARCHAR(length=20), nullable=True)
        ps3_rel = relationship('CompetencyHub', backref="ps3")

        def __int__(self, id, text):
            self.id = id
            self.text = text

    class Language(Base):
        __tablename__ = 'language'

        id = Column(Integer, primary_key=True, nullable=False)
        lang_name = Column(VARCHAR, nullable=False)
        lan_rel = relationship('CompetencyHub', backref="lang")

        def __init__(self, lang_name):
            self.lang_name = lang_name

    class RDCT(Base):
        __tablename__ = 'RDCT'

        id = Column(Integer, primary_key=True, nullable=False)
        rdct_name = Column(VARCHAR, nullable=False)
        rdct_rel = relationship('CompetencyHub', backref="rdct")

        def __init__(self, rdct_name):
            self.rdct_name = rdct_name

    class Practices(Base):
        __tablename__ = 'Practices'

        id = Column(Integer, primary_key=True, nullable=False)
        name = Column(VARCHAR, nullable=False)
        prac_rel = relationship('CompetencyHub', backref="prac")

        def __init__(self, name_p):
            self.name = name_p

    class CompetencyHub(Base):
        __tablename__ = 'competency_hub'

        id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
        emp_id = Column(Integer, ForeignKey('Employee.emp_id'), nullable=False)
        emp_lang_id = Column(Integer, ForeignKey('language.id'), nullable=False)
        emp_practice_id = Column(Integer, ForeignKey('Practices.id'), nullable=False)
        emp_rdct_id = Column(Integer, ForeignKey('RDCT.id'), nullable=False)
        tech_id = Column(Integer, ForeignKey('Technology.id'), nullable=False)
        micro_id = Column(Integer, ForeignKey('Microcontroller.id'), nullable=False)
        offering_id = Column(Integer, ForeignKey('Offering.id'), nullable=False)
        tools_id = Column(Integer, ForeignKey('Tools.id'), nullable=False)
        company_id = Column(Integer, ForeignKey('Company.id'), nullable=False)
        ps1_id = Column(Integer, ForeignKey('Ps1.id'), nullable=False)
        ps2_id = Column(Integer, ForeignKey('Ps2.id'), nullable=False)
        ps3_id = Column(Integer, ForeignKey('Ps3.id'), nullable=False)
        level = Column(Integer, ForeignKey('levels.id'), nullable=False)

        def __init__(self, emp_id, emp_lang_id, emp_practice_id, emp_rdct_id, level, tech_id, micro_id, offering_id,
                     tools_id, company_id, ps1_id, ps2_id, ps3_id):
            self.level = level
            self.emp_id = emp_id
            self.emp_lang_id = emp_lang_id
            self.emp_practice_id = emp_practice_id
            self.emp_rdct_id = emp_rdct_id
            self.tech_id = tech_id
            self.micro_id = micro_id
            self.offering_id = offering_id
            self.tools_id = tools_id
            self.company_id = company_id
            self.ps1_id = ps1_id
            self.ps2_id = ps2_id
            self.ps3_id = ps3_id

    if not isinstance(names, (str, list)) and names is not None:
        raise TypeError("names must be None, a String or list of Strings")

    if isinstance(names, str):
        if names in locals().keys() and inspect.isclass(locals()[names]) and hasattr(locals()[names],
                                                                                     "_sa_class_manager"):
            return locals()[names]
        return None

    if names is None:
        names = list(locals().keys())

    classess = {}
    for name in names:
        if name in locals().keys():
            local = locals()[name]
            if inspect.isclass(local) and hasattr(local, "_sa_class_manager"):
                classess[name] = local

    return classess
