from datetime import datetime, date
from peewee import *
from app.db.database import db

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    """
    Represents an individual user of the application.
    """
    id = AutoField()
    username = CharField(unique=True, index=True, max_length=50)
    email = CharField(unique=True, index=True, max_length=255)
    hashed_password = CharField(max_length=100)
    is_superuser = BooleanField(default=False)

    class Meta:
        table_name = "user"

class Group(BaseModel):
    """
    Represents a private group of friends for movie tracking.
    """
    id = AutoField()
    name = CharField(unique=True, index=True, max_length=100)
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "group"

class UserGroupLink(BaseModel):
    """
    Links Users to Groups, forming a many-to-many relationship.
    Each entry represents a user's membership in a specific group.
    """
    user = ForeignKeyField(User, backref='group_links', on_delete='CASCADE')
    group = ForeignKeyField(Group, backref='member_links', on_delete='CASCADE')
    joined_at = DateTimeField(default=datetime.now)

    class Meta:
        primary_key = CompositeKey('user', 'group')
        table_name = "usergrouplink"

class Movie(BaseModel):
    """
    Represents a movie in your internal catalog.
    It links to TMDb via tmdb_id and caches frequently accessed details.
    """
    id = AutoField()
    tmdb_id = CharField(unique=True, index=True, max_length=20)
    title = CharField(index=True, max_length=255)
    release_year = IntegerField(null=True, index=True)
    poster_url = TextField(null=True)

    class Meta:
        table_name = "movie"

class Poll(BaseModel):
    """
    Represents a poll created within a group to decide on a movie.
    """
    id = AutoField()
    group = ForeignKeyField(Group, backref='polls', on_delete='CASCADE')
    creator = ForeignKeyField(User, backref='polls_created', on_delete='RESTRICT')
    title = CharField(max_length=255)
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)
    expires_at = DateTimeField(null=True)
    is_active = BooleanField(default=True, index=True)
    resolved_at = DateTimeField(null=True)
    winning_poll_option = DeferredForeignKey('PollOption', backref='winning_poll', null=True, on_delete='SET NULL')

    class Meta:
        table_name = "poll"

class PollOption(BaseModel):
    """
    Represents a single movie suggestion within a poll.
    """
    id = AutoField()
    poll = ForeignKeyField(Poll, backref='options', on_delete='CASCADE')
    movie_details = ForeignKeyField(Movie, backref='poll_options', on_delete='RESTRICT') # Don't delete movie if it's a poll option
    suggested_by = ForeignKeyField(User, backref='poll_options_suggested', on_delete='RESTRICT')
    suggested_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "polloption"
        indexes = (
            (('poll', 'movie_details'), True),
        )

class Vote(BaseModel):
    """
    Represents a single vote cast by a user for a poll option.
    """
    poll_option = ForeignKeyField(PollOption, backref='votes', on_delete='CASCADE')
    voter = ForeignKeyField(User, backref='votes_cast', on_delete='RESTRICT')
    poll_context = ForeignKeyField(Poll, backref='votes', on_delete='CASCADE')
    voted_at = DateTimeField(default=datetime.now)

    class Meta:
        primary_key = CompositeKey('poll_context', 'voter')
        table_name = "vote"

class WatchedMovie(BaseModel):
    """
    Records a movie that a group has watched together.
    This is your primary "history" table.
    """
    id = AutoField()
    movie_details = ForeignKeyField(Movie, backref='watched_entries', on_delete='RESTRICT')
    group = ForeignKeyField(Group, backref='watched_movies_history', on_delete='CASCADE')
    watched_date = DateField(default=date.today)
    logged_by_user = ForeignKeyField(User, backref='watched_movies_logged', on_delete='RESTRICT')
    notes = TextField(null=True)
    originating_poll = ForeignKeyField(Poll, backref='resulting_watched_movie', null=True, unique=True, on_delete='SET NULL')

    class Meta:
        table_name = "watchedmovie"

class MovieRating(BaseModel):
    """
    Represents a user's rating for a specific watched movie entry.
    """
    watched_movie_entry = ForeignKeyField(WatchedMovie, backref='ratings', on_delete='CASCADE')
    rater = ForeignKeyField(User, backref='movie_ratings', on_delete='RESTRICT')
    rating_value = IntegerField()
    rated_at = DateTimeField(default=datetime.now)

    class Meta:
        primary_key = CompositeKey('watched_movie_entry', 'rater')
        table_name = "movierating"

TABLES_TO_CREATE = [
    User,
    Group,
    Movie,
    UserGroupLink,
    Poll,
    PollOption,
    Vote,
    WatchedMovie,
    MovieRating
]

