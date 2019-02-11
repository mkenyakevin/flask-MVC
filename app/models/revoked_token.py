from orator import Model


class RevokedTokens(Model):
    __table__ = 'revoked_tokens'
    __guarded__ = ['id']
    pass
