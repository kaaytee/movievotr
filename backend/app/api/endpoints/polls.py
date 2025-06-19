from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/groups/{group_id}/polls", response_model=schemas.Poll, status_code=status.HTTP_201_CREATED)
def create_poll_in_group(
    group_id: int,
    poll_in: schemas.PollCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Create a new poll within a specific group.
    User must be a member of the group.
    """
    group = crud.crud_group.get_group_by_id(group_id=group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if not crud.crud_group.is_user_member_of_group(user=current_user, group=group):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this group")

    # Verify all movie_ids exist in our catalog
    for movie_id in poll_in.movie_ids:
        if not crud.crud_movie.Movie.get_or_none(id=movie_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie with id {movie_id} not found in catalog.")

    return crud.crud_poll.create_poll(poll_in=poll_in, group=group, creator=current_user)


@router.get("/groups/{group_id}/polls", response_model=List[schemas.Poll])
def list_active_polls_in_group(
    group_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    List active polls for a group.
    User must be a member of the group.
    """
    group = crud.crud_group.get_group_by_id(group_id=group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if not crud.crud_group.is_user_member_of_group(user=current_user, group=group):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this group")
        
    return crud.crud_poll.get_active_polls_for_group(group=group)


@router.get("/{poll_id}", response_model=Any) # Using Any for custom dict response
def get_poll_details(
    poll_id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get details of a specific poll, including options and current vote counts.
    User must be a member of the poll's group.
    """
    poll = crud.crud_poll.get_poll_by_id(poll_id=poll_id)
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")

    if not crud.crud_group.is_user_member_of_group(user=current_user, group=poll.group):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this poll's group")
    
    poll_data = schemas.Poll.model_validate(poll).dict()
    poll_data['vote_counts'] = crud.crud_poll.get_vote_counts_for_poll(poll=poll)
    
    return poll_data


@router.post("/{poll_id}/vote", response_model=schemas.Vote)
def vote_on_poll(
    poll_id: int,
    vote_in: schemas.VoteCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Cast a vote for a poll option.
    User must be a member of the poll's group.
    """
    poll = crud.crud_poll.get_poll_by_id(poll_id=poll_id)
    if not poll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")
        
    if not poll.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This poll is no longer active.")

    if not crud.crud_group.is_user_member_of_group(user=current_user, group=poll.group):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this poll's group")

    try:
        vote = crud.crud_poll.cast_vote(vote_in=vote_in, poll=poll, voter=current_user)
        return vote
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) 