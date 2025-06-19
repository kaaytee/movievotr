from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.crud import crud_user, crud_group, crud_poll
from app import models, schemas
from app.schemas.poll import Poll, PollCreate
from app.schemas.group import GroupWithMembers
from app.api import deps

router = APIRouter()

@router.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_superuser)
):
    """
    Retrieve all users.
    """
    users = crud_user.get_users(skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_superuser)
):
    """
    Get a specific user by ID.
    """
    user = crud_user.get_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_superuser)
):
    """
    Delete a user.
    """
    user = crud_user.get_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Admins cannot delete their own account")

    deleted_user = crud_user.delete_user(user_id=user_id)
    return deleted_user

@router.get("/groups/", response_model=List[schemas.Group])
def read_groups(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_superuser)
):
    """
    Retrieve all groups.
    """
    groups = crud_group.get_groups(skip=skip, limit=limit)
    return groups

@router.get("/groups/{group_id}", response_model=GroupWithMembers)
def read_group(
    group_id: int,
    current_user: models.User = Depends(deps.get_current_superuser)
):
    """
    Get a specific group by ID, including its members.
    """
    group = crud_group.get_group_by_id(group_id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Attach members to the group object so Pydantic can build the response model
    group.members = crud_group.get_all_members(group=group)
    return group

@router.delete("/groups/{group_id}", response_model=schemas.Group)
def delete_group(
    group_id: int,
    current_user: models.User = Depends(deps.get_current_superuser)
):
    """
    Delete a group.
    """
    group = crud_group.get_group_by_id(group_id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    deleted_group = crud_group.delete_group(group_id=group_id)
    return deleted_group

# --- Poll Admin Endpoints ---

@router.get("/polls/", response_model=List[Poll])
def read_polls(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_superuser)
):
    """
    Retrieve all polls.
    """
    polls = crud_poll.get_polls(skip=skip, limit=limit)
    return polls

@router.get("/polls/{poll_id}", response_model=Poll)
def read_poll(
    poll_id: int,
    current_user: models.User = Depends(deps.get_current_superuser)
):
    """
    Get a specific poll by ID.
    """
    poll = crud_poll.get_poll_by_id(poll_id=poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

@router.post("/polls/", response_model=Poll)
def create_poll(
    poll_in: PollCreate,
    group_id: int,
    creator_id: int,
    current_user: models.User = Depends(deps.get_current_superuser)
):
    """
    Create a poll as admin for any group and creator.
    """
    group = crud_group.get_group_by_id(group_id)
    creator = crud_user.get_user(creator_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    poll = crud_poll.create_poll(poll_in=poll_in, group=group, creator=creator)
    return poll
