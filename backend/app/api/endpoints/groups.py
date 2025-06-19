from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, models, schemas
from app.crud import crud_group
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Group, status_code=status.HTTP_201_CREATED)
def create_new_group(
    group_in: schemas.GroupCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Create a new group. The current user becomes the first member.
    """
    return crud_group.create_group(group_in=group_in, creator=current_user)

@router.get("/", response_model=List[schemas.Group])
def read_user_groups(
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    List all groups the current user is a member of.
    """
    return crud_group.get_groups_for_user(user=current_user)

@router.post("/{group_id}/join", response_model=schemas.Group)
def join_group(
    group_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Allow the current user to join an existing group.
    """
    group = crud_group.get_group_by_id(group_id=group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    
    if crud_group.is_user_member_of_group(user=current_user, group=group):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a member of this group")
        
    crud_group.add_user_to_group(user=current_user, group=group)
    return group

@router.get("/{group_id}", response_model=schemas.Group)
def read_group_details(
    group_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get details of a specific group, only if the user is a member.
    """
    group = crud_group.get_group_by_id(group_id=group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if not crud_group.is_user_member_of_group(user=current_user, group=group):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this group")

    return group 