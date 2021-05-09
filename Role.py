class Role(object):
    role_name = ''
    permissions = []

    def __init__(self, role_name, permissions):
        self.role_name = role_name
        self.permissions = permissions

    def add_permission_to_role(self, action_type, resource):
        permission_string = action_type + '$' + resource
        self.permissions.append(permission_string)
        print(f'permission {action_type} {resource} '
              f'added successfully to the role {self.role_name}')

    def view_all_permissions(self):
        print(f'Role - {self.role_name} has permissions {self.permissions}')

    def remove_permission_from_role(self, permission):
        self.permissions.remove(permission)