class User(object):
    roles = []
    name = None

    def __init__(self, name, roles):
        self.name = name
        self.roles = roles

    def add_role_to_user(self, role_name):
        self.roles.append(role_name)
        print(f'User roles after adding "{role_name}" --{self.roles}')

    def view_user_roles(self):
        print(f'This user has following roles {self.roles}')

    def remove_role_from_user(self, role_name):
        self.roles.remove(role_name)
        print(f'User roles after removing "{role_name}" --{self.roles}')

    def check_permissions(self, action_type, resource):
        permission = action_type+'$'+resource
        # print(permission)
        for role in self.roles:
            if permission in role.permissions:
                return True
        return False
