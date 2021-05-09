# from __future__ import absolute_import
from User import User
from Role import Role
import functools

SAMPLE_RESOURCES = ['user', 'role']

ACTION_TYPES = ['read', 'write', 'update', 'delete']

USERS_MAP = {}
ROLES_MAP = {}


def check_permissions(action_type, resource):
    def check_permissions_decorator(function):
        @functools.wraps(function)
        def wrapper():
            user = CURRENT_USER
            print(user.name)
            if user.check_permissions(action_type,resource):
                return function()
            else:
                return lambda: f"You dont have {action_type} permission on resource {resource}"
        return wrapper
    return check_permissions_decorator


print('-----ROLE BASED AUTH CONTROL SYSTEM-----')

# creating admin role
admin_permissions = [action + '$' + resource for action in ACTION_TYPES for resource in SAMPLE_RESOURCES]
# print(admin_permissions)
admin_role = Role('admin_role', admin_permissions)
ROLES_MAP[admin_role.role_name] = admin_role

#creat read role
# read_role = Role('read_role', ['read$user'])
# ROLES_MAP[read_role.role_name] = read_role

# create admin user
admin_user = User('admin_user', [admin_role, ])
USERS_MAP[admin_user.name] = admin_user

CURRENT_USER = admin_user


def switch_user():
    switch_user_to = input('Provide user name to login\n')
    if switch_user_to in USERS_MAP:
        global CURRENT_USER
        CURRENT_USER = USERS_MAP[switch_user_to]
        return f'Successfully logged in as {switch_user_to}'
    return "User not found"


# @check_permissions('write', 'user')
def create_user():
    if CURRENT_USER.check_permissions('write','user'):
        user_name = input('Enter user name: \n')
        role = ROLES_MAP.get(input('Add one role name to add it to the user:\n'))
        if not role:
            return 'No role found'
        new_user = User(user_name, [role,])
        USERS_MAP[user_name] = new_user
        return 'User successfully created'
    return "You dont have required permissions"

def create_role():
    if CURRENT_USER.check_permissions('write','role'):
        role_name = input('Enter role name: \n')
        permission = input('Enter permission in format "action$resource"\n')
        new_role = Role(role_name, [permission,])
        ROLES_MAP[role_name] = new_role
        return 'Role created successfully'
    return 'You dont have permission'

def add_permission_to_role():
    if CURRENT_USER.check_permissions('update','role'):
        role_name = input('Enter role name: \n')
        permission = input('Enter permission to add in format "action$resource"\n')
        role = ROLES_MAP.get(role_name)
        if role:
            role.permissions.append(permission)
            return 'Permission added'
        return 'Role not found'
    return 'You dont have permission'

def remove_permission_to_role():
    if CURRENT_USER.check_permissions('update','role'):
        role_name = input('Enter role name: \n').strip()
        permission = input('Enter permission to remove in format "action$resource"\n').strip()
        role = ROLES_MAP.get(role_name)
        if role:
            if permission in role.permissions:
                role.permissions.remove(permission)
                return 'Permission removed'
            else:
                return 'Role does not have this permission'
        return 'Role not found'
    return 'You dont have permission'

def add_role_to_user():
    if CURRENT_USER.check_permissions('update','user'):
        user_name = input('Enter Username\n').strip()
        user = USERS_MAP.get(user_name)
        if not user:
            return 'No user found'
        role_name = input('Enter role name\n')
        role = ROLES_MAP.get(role_name)
        if not role:
            return 'No role found'

        user.roles.extend(role)
        return 'Role added successfully'
    return 'You dont have permission'

def remove_role_from_user():
    if CURRENT_USER.check_permissions('update','user'):
        user_name = input('Enter Username\n').strip()
        user = USERS_MAP.get(user_name)
        if not user:
            return 'No user found'
        role_name = input('Enter role name\n')
        role = ROLES_MAP.get(role_name)
        if not role:
            return 'No role found'
        if role in user.roles:
            user.roles.remove(role)
            return 'Role removed successfully'
        else:
            return 'User does not have this role'
    return 'You dont have permission'


def view_all_roles():
    if CURRENT_USER.check_permissions('read','user'):
        return [role.role_name for role in CURRENT_USER.roles]
    return 'You dont have permission'


def view_all_permissions():
    if CURRENT_USER.check_permissions('read','user'):
        return [','.join(role.permissions) for role in CURRENT_USER.roles]
    return 'You dont have permission'

def exit_system():
    exit()

command_line_actions = {
    '0': exit_system,
    '1': switch_user,
    '2': create_user,
    '3': create_role,
    '4': add_permission_to_role,
    '5': remove_permission_to_role,
    '6': add_role_to_user,
    '7': remove_role_from_user,
    '8': view_all_roles,
    '9': view_all_permissions
}

while True:
    print(f'Hi! You have logged in as {CURRENT_USER.name}')
    print('''
ACTIONS:
-------------------------
press 1  to login as another user
press 2 to create user
press 3 to create role
press 4 to add permission to role
press 5 to remove permission from role
press 6 to add role to user
press 7 to remove role from user
press 8 to view roles for current user
press 9 to view all permissions for current user
press 0 to exit
            ''')
    user_input = input()
    action_result = command_line_actions.get(user_input, lambda: 'Invalid Input')()
    print(action_result)

    next_action = input('Press 1 to continue..')
    if not next_action == '1':
        break

