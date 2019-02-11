from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.increments('id')
            table.string('username').unique()
            table.string('email').unique().nullable()
            table.string('phone_number').unique()
            table.string('password')
            table.integer('role_id').unsigned()
            table.foreign('role_id').references('id').on('roles')
            table.soft_deletes()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
