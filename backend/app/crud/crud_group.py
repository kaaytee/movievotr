from typing import List, Optional
from app.models.model import Group, User, UserGroupLink
from app.schemas.group import GroupCreate

def create_group(group_in: GroupCreate, creator: User) -> Group:
    """
    Creates a new group and adds the creator as the first member.
    """
    group = Group.create(name=group_in.name, description=group_in.description)
    UserGroupLink.create(user=creator, group=group)
    return group

def get_all_members(group: Group) -> List[User]:
    """
    Retrieves all members of a group.
    """
    return list(User.select().join(UserGroupLink).where(UserGroupLink.group == group))



def get_group_by_id(group_id: int) -> Group:
    """
    Retrieves a group by its ID.
    """
    return Group.get_or_none(Group.id == group_id)

def get_groups_for_user(user: User) -> List[Group]:
    """
    Retrieves all groups a user is a member of.
    """
    return (Group
            .select()
            .join(UserGroupLink)
            .where(UserGroupLink.user == user))

def is_user_member_of_group(user: User, group: Group) -> bool:
    """
    Checks if a user is a member of a specific group.
    """
    return UserGroupLink.get_or_none((UserGroupLink.user == user) & (UserGroupLink.group == group)) is not None

def add_user_to_group(user: User, group: Group):
    """
    Adds a user to a group.
    """
    if not is_user_member_of_group(user, group):
        UserGroupLink.create(user=user, group=group)

def get_groups(skip: int = 0, limit: int = 100) -> List[Group]:
    """ 
    Retrieves a list of groups with pagination.
    """
    return list(Group.select().offset(skip).limit(limit))

def delete_group(group_id: int) -> Optional[Group]:
    """
    Deletes a group from the database.
    """
    group = get_group_by_id(group_id=group_id)
    if group:
        group.delete_instance(recursive=True)
    return group