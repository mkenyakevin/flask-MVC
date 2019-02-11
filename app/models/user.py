from orator import Model


class Users(Model):
    __table__ = 'users'
    __guarded__ = ['id']

    # def check_password(self, password):
    #    return flask_bcrypt.check_password_hash(self.password_hash, password)

    pass
