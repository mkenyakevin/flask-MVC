from orator.migrations import Migration


class CreateRevokedTokensTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('revoked_tokens') as table:
            table.increments('id')
            table.string('jti')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('revoked_tokens')
