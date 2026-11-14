from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKey, Index, String
from sqlalchemy import CheckConstraint, ForeignKey, Index, JSON, String, UniqueConstraint
from pydantic import AwareDatetime
from sqlalchemy.dialects.sqlite import insert


class Base(DeclarativeBase):
    pass

class Athlete(Base):
    __tablename__ = "athletes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    pseudonym: Mapped[str] = mapped_column(String(80), unique=True)
    created_at: Mapped[str] = mapped_column(String(32))
class ExerciseSession(Base):
    __tablename__ = "exercise_sessions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('in_progress', 'finished', 'cancelled')",
            name="ck_exercise_sessions_status",
        ),
        Index("idx_sessions_athlete_date", "athlete_id", "started_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    athlete_id: Mapped[str] = mapped_column(ForeignKey("athletes.id"))
    exercise_code: Mapped[str] = mapped_column(String(80))
    protocol_id: Mapped[str] = mapped_column(String(80))
    protocol_version: Mapped[str] = mapped_column(String(32))
    started_at: Mapped[str] = mapped_column(String(32))
    ended_at: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(20))
    load_kg: Mapped[float | None]
    target_repetitions: Mapped[int | None]
    rep_count: Mapped[int] = mapped_column(server_default="0")
class MotionSample(Base):
    __tablename__ = "motion_samples"
    __table_args__ = (
        UniqueConstraint("session_id", "frame_id", name="uq_motion_samples_session_frame"),
        CheckConstraint("frame_id >= 0", name="ck_motion_samples_frame_id"),
        CheckConstraint("quality BETWEEN 0 AND 1", name="ck_motion_samples_quality"),
        CheckConstraint(
            "image_width > 0 AND image_height > 0",
            name="ck_motion_samples_image_dimensions",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("exercise_sessions.id"))
    frame_id: Mapped[int]
    captured_at: Mapped[str] = mapped_column(String(32))
    angles_json: Mapped[dict[str, float]] = mapped_column(JSON)
    quality: Mapped[float]
    image_width: Mapped[int]
    image_height: Mapped[int]
    landmarks_version: Mapped[str] = mapped_column(String(80))
