from typing import List, Optional
from app.models.model import Poll, PollOption, Vote, Group, User, Movie
from app.schemas.poll import PollCreate
from app.schemas.vote import VoteCreate

def create_poll(poll_in: PollCreate, group: Group, creator: User) -> Poll:
    """
    Creates a new poll and its associated options in the database.
    """
    poll = Poll.create(
        group=group,
        creator=creator,
        title=poll_in.title,
        description=poll_in.description,
        expires_at=poll_in.expires_at
    )
    
    for movie_id in poll_in.movie_ids:
        movie = Movie.get_or_none(Movie.id == movie_id)
        if movie:
            PollOption.create(
                poll=poll,
                movie_details=movie,
                suggested_by=creator
            )

    return poll

def get_poll_by_id(poll_id: int) -> Optional[Poll]:
    """
    Retrieves a poll by its ID.
    """
    return Poll.get_or_none(Poll.id == poll_id)

def get_polls(skip: int = 0, limit: int = 100) -> List[Poll]:
    """
    Retrieves all polls with pagination.
    """
    return list(Poll.select().offset(skip).limit(limit))

def get_active_polls_for_group(group: Group) -> List[Poll]:
    """
    Retrieves all active polls for a specific group.
    """
    return (Poll
            .select()
            .where((Poll.group == group) & (Poll.is_active == True)))

def cast_vote(vote_in: VoteCreate, poll: Poll, voter: User) -> Vote:
    """
    Casts a vote for a poll option.
    Handles the "one vote per user per poll" logic.
    """
    existing_vote = Vote.get_or_none((Vote.poll_context == poll) & (Vote.voter == voter))
    if existing_vote:
        raise ValueError("User has already voted in this poll.")

    poll_option = PollOption.get_or_none((PollOption.id == vote_in.poll_option_id) & (PollOption.poll == poll))
    if not poll_option:
        raise ValueError("Poll option not found in this poll.")

    vote = Vote.create(
        poll_option=poll_option,
        voter=voter,
        poll_context=poll
    )
    return vote

def get_poll_option_by_id(poll_option_id: int) -> Optional[PollOption]:
    """
    Retrieves a poll option by its ID.
    """
    return PollOption.get_or_none(PollOption.id == poll_option_id)

def get_vote_counts_for_poll(poll: Poll) -> dict:
    """
    Calculates the vote counts for each option in a poll.
    Returns a dictionary of {poll_option_id: vote_count}.
    """
    counts = {}
    for option in poll.options:
        counts[option.id] = option.votes.count()
    return counts 