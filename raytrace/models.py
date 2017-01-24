from sqlalchemy import Column, String, Float
from tropofy.database.tropofy_orm import DataSetMixin, UniqueConstraint, ForeignKeyConstraint

# database models

class Material(DataSetMixin):
    name = Column(String(25))
    red = Column(Float)
    green = Column(Float)
    blue = Column(Float)
    reflectance = Column(Float)

    def __str__(self): # type: () -> str
        return self.name

    @classmethod
    def get_table_args(cls):
        return UniqueConstraint('name', 'data_set_id'),


class Sphere(DataSetMixin):
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    radius = Column(Float)
    material = Column(String(25))

    @classmethod
    def get_table_args(cls):
        return ForeignKeyConstraint(['material', 'data_set_id'],
                                    ['material.name', 'material.data_set_id'],
                                    ondelete='CASCADE', onupdate='CASCADE'),


class Light(DataSetMixin):
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    power = Column(Float)
