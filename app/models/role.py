from orator import Model


class Roles(Model):
    __table__ = 'roles'
    __guarded__ = ['id']
    pass
