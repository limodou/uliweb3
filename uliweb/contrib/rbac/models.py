from uliweb.orm import *

class Permission(Model):
    name = Field(str, max_length=80, required=True)
    description = Field(str, max_length=255)
    props = Field(PICKLE)
    
    def get_users(self):
        for role in self.perm_roles.all():
            for u in role.users.all():
                yield u
                
    def get_users_ids(self):
        for role in self.perm_roles.all():
            for u in role.users.ids():
                yield u
    
class Role(Model):
    name = Field(str, max_length=80, required=True)
    description = Field(str, max_length=255)
    reserve = Field(bool)
    users = ManyToMany('user', collection_name='user_roles')
    permissions = ManyToMany('permission', through='role_perm_rel', collection_name='perm_roles')
    usergroups = ManyToMany('usergroup', collection_name='usergroup_roles')
    
    def usergroups_has_user(self,user):
        for usergroup in list(self.usergroups.all()):
            if usergroup.users.has(user):
                return usergroup
        return False
    
class Role_Perm_Rel(Model):
    role = Reference('role')
    permission = Reference('permission')
    props = Field(PICKLE)
    
    
