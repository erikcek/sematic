# Standard library
import datetime
import typing

# Third party
from sqlalchemy import Column, types
from sqlalchemy.orm import validates

# Glow
from glow.abstract_future import FutureState
from glow.db.models.base import Base


class Run(Base):
    """
    SQLAlchemy model for runs.

    Runs represent the execution of a :class:`glow.Calculator`. They are
    created upon scheduling of a :class:`glow.Future`.

    Attributes
    ----------
    id : str
        The UUID4 of the run.
    future_state : str
        The state of the corresponding :class:`glow.Future`. See
        :class:`glow.abstract_future.FutureState` for possible values.
    name : str
        The name of the run. Defaults to the name of the :class:`glow.Calculator`.
    calculator_path : str
        The full import path of the :class:`glow.Calculator`.
    parent_id : Optional[str]
        The id of the parent run. A parent run is the run corresponding to
        the :class:`glow.Calculator` encapsulating the current
        :class:`glow.Calculator`.
    created_at : datetime
        Time of creating of the run record in the DB.
    updated_at : datetime
        Time of last update of the run record in the DB.
    started_at : Optional[datetime]
        Time at which the run has actually started executing.
    ended_at : Optional[datetime]
        Time at which the run has finished running.
    resolved_at : Optional[datetime]
        Time at which the run has a concrete resolved value.
        This is different from `ended_at` if the :class:`glow.Calculator`
        returns a :class:`glow.Future`.
    failed_at : Optional[datetime]
        Time at which the run has failed.

    """

    __tablename__ = "runs"

    id: str = Column(types.String(), primary_key=True)
    future_state: str = Column(types.String(), nullable=False)
    name: str = Column(types.String(), nullable=True)
    calculator_path: str = Column(types.String(), nullable=False)
    parent_id: typing.Optional[str] = Column(types.String(), nullable=True)

    # Lifecycle timestamps
    created_at: datetime.datetime = Column(
        types.DateTime(), nullable=False, default=datetime.datetime.utcnow
    )
    updated_at: datetime.datetime = Column(
        types.DateTime(),
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    started_at: typing.Optional[datetime.datetime] = Column(
        types.DateTime(), nullable=True
    )
    ended_at: typing.Optional[datetime.datetime] = Column(
        types.DateTime(), nullable=True
    )
    resolved_at: typing.Optional[datetime.datetime] = Column(
        types.DateTime(), nullable=True
    )
    failed_at: typing.Optional[datetime.datetime] = Column(
        types.DateTime(), nullable=True
    )

    @validates("future_state")
    def validate_future_state(self, key, value) -> str:
        """
        Validates that the future_state value is allowed.
        """
        if value not in FutureState.values():
            raise ValueError(
                (
                    "The value of `Run.future_state`"
                    " must be one of the values in `FutureState`."
                )
            )
        return value