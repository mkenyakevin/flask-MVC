from orator.seeds import Seeder


class CreateRolesTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('roles').insert({
            'role_name': 'Super Admin',
            'description': 'He is in charge of the entire system',
            'role_code': '001'
        })
        self.db.table('roles').insert({
            'role_name': 'Admin',
            'description': 'He is in charge of the organisation',
            'role_code': '002'
        })
        self.db.table('roles').insert({
            'role_name': 'Manager',
            'description': 'He is in charge of one store',
            'role_code': '003'
        })
        self.db.table('roles').insert({
            'role_name': 'Cashier',
            'description': 'He is in charge of sales in a store',
            'role_code': '004'
        })
        pass
