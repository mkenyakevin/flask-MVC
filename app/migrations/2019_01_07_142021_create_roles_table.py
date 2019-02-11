from orator.migrations import Migration


class CreateRolesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('roles') as table:
            table.increments('id')
            table.string('role_name')
            table.text('description')
            table.string('role_code')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('roles')
