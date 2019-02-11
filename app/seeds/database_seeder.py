from orator.seeds import Seeder

from seeds.create_roles_table_seeder import CreateRolesTableSeeder


class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(CreateRolesTableSeeder)
        pass

