from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import update
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AwareDatetime, BaseModel, Field, FiniteFloat
from models import Athlete, ExerciseSession
from models import Athlete, ExerciseSession, MotionSample

from database import engine
from models import Athlete

app = FastAPI(title="ORION")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    try:
        with Session(engine) as db:
            db.execute(select(Athlete.id).limit(1))
            db.execute(select(ExerciseSession.id).limit(1))
            db.execute(select(MotionSample.id).limit(1))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=503,
            detail="Banco de dados indisponível ou esquema incompleto.",
        ) from error

    return {"status": "ready", "database": "ok"}
class AthleteCreate(BaseModel):
    pseudonym: str


@app.post("/api/v1/athletes", status_code=201)
def create_athlete(payload: AthleteCreate):
    pseudonym = payload.pseudonym.strip()
    if not 1 <= len(pseudonym) <= 80:
        raise HTTPException(422, "O pseudônimo deve ter entre 1 e 80 caracteres.")

    athlete = Athlete(
        id=str(uuid4()),
        pseudonym=pseudonym,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )

    with Session(engine) as db:
        db.add(athlete)
        try:
            db.commit()
        except IntegrityError as error:
            db.rollback()
            if getattr(error.orig, "sqlite_errorname", None) == "SQLITE_CONSTRAINT_UNIQUE":
                raise HTTPException(409, "Esse pseudônimo já está cadastrado.") from error
            raise

        return {
            "id": athlete.id,
            "pseudonym": athlete.pseudonym,
            "created_at": athlete.created_at,
        }
@app.get("/api/v1/athletes/{athlete_id}")
def get_athlete(athlete_id: UUID):
    with Session(engine) as db:
        athlete = db.get(Athlete, str(athlete_id))

        if athlete is None:
            raise HTTPException(404, "Perfil não encontrado.")

        return {
            "id": athlete.id,
            "pseudonym": athlete.pseudonym,
            "created_at": athlete.created_at,
        }
class ExerciseSessionCreate(BaseModel):
    athlete_id: UUID
    exercise_code: str
    protocol_id: str
    load_kg: FiniteFloat | None = Field(default=None, ge=0)
    target_repetitions: int | None = Field(default=None, gt=0)


@app.post("/api/v1/sessions", status_code=201)
def create_exercise_session(payload: ExerciseSessionCreate):
    with Session(engine) as db:
        athlete_id = str(payload.athlete_id)

        if db.get(Athlete, athlete_id) is None:
            raise HTTPException(404, "Perfil não encontrado.")

        if (payload.exercise_code, payload.protocol_id) != ("squat", "SQUAT-01"):
            raise HTTPException(422, "Protocolo indisponível para esse exercício.")

        session = ExerciseSession(
            id=str(uuid4()),
            athlete_id=athlete_id,
            exercise_code=payload.exercise_code,
            protocol_id=payload.protocol_id,
            protocol_version="1",
            started_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            status="in_progress",
            load_kg=payload.load_kg,
            target_repetitions=payload.target_repetitions,
        )

        db.add(session)
        db.commit()

        return {
            "session_id": session.id,
            "status": session.status,
            "started_at_utc": session.started_at,
            "protocol_version": session.protocol_version,
        }
class MotionSampleCreate(BaseModel):
    frame_id: int = Field(ge=0, le=2**63 - 1)
    captured_at_utc: AwareDatetime
    pose_quality: FiniteFloat = Field(ge=0, le=1)
    angles_deg: dict[str, FiniteFloat]
    image_width: int = Field(gt=0)
    image_height: int = Field(gt=0)
    landmarks_version: str = Field(min_length=1, max_length=80)


class MotionSampleBatch(BaseModel):
    samples: list[MotionSampleCreate] = Field(min_length=1, max_length=50)


@app.post("/api/v1/sessions/{session_id}/samples")
def add_motion_samples(session_id: UUID, payload: MotionSampleBatch):
    with Session(engine) as db:
        exercise_session = db.get(ExerciseSession, str(session_id))

        if exercise_session is None:
            raise HTTPException(404, "Sessão não encontrada.")

        if exercise_session.status != "in_progress":
            raise HTTPException(409, "A sessão precisa estar em andamento.")

        rows = [
            {
                "id": str(uuid4()),
                "session_id": str(session_id),
                "frame_id": sample.frame_id,
                "captured_at": sample.captured_at_utc.astimezone(timezone.utc).isoformat(),
                "angles_json": sample.angles_deg,
                "quality": sample.pose_quality,
                "image_width": sample.image_width,
                "image_height": sample.image_height,
                "landmarks_version": sample.landmarks_version,
            }
            for sample in payload.samples
        ]

        statement = (
            insert(MotionSample)
            .values(rows)
            .on_conflict_do_nothing(index_elements=["session_id", "frame_id"])
        )
        result = db.execute(statement)
        inserted = result.rowcount
        db.commit()

        return {
            "received": len(rows),
            "inserted": inserted,
            "duplicates": len(rows) - inserted,
        }
@app.post("/api/v1/sessions/{session_id}/finish")
def finish_exercise_session(session_id: UUID):
    with Session(engine) as db:
        statement = (
            update(ExerciseSession)
            .where(
                ExerciseSession.id == str(session_id),
                ExerciseSession.status == "in_progress",
            )
            .values(
                status="finished",
                ended_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            )
        )

        db.execute(statement)
        exercise_session = db.get(ExerciseSession, str(session_id))

        if exercise_session is None:
            raise HTTPException(404, "Sessão não encontrada.")

        if exercise_session.status != "finished":
            raise HTTPException(409, "A sessão está cancelada.")

        result = {
            "session_id": exercise_session.id,
            "status": exercise_session.status,
            "ended_at_utc": exercise_session.ended_at,
            "rep_count": exercise_session.rep_count,
        }
        db.commit()
        return result
@app.get("/api/v1/sessions")
@app.get("/api/v1/sessions")
def list_exercise_sessions(
    athlete_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    with Session(engine) as db:
        athlete_key = str(athlete_id)

        if db.get(Athlete, athlete_key) is None:
            raise HTTPException(404, "Perfil não encontrado.")

        statement = (
            select(ExerciseSession)
            .where(ExerciseSession.athlete_id == athlete_key)
            .order_by(ExerciseSession.started_at.desc(), ExerciseSession.id.desc())
            .limit(limit)
            .offset(offset)
        )

        return [
            {
                "session_id": session.id,
                "exercise_code": session.exercise_code,
                "protocol_id": session.protocol_id,
                "status": session.status,
                "started_at_utc": session.started_at,
                "ended_at_utc": session.ended_at,
                "rep_count": session.rep_count,
            }
            for session in db.scalars(statement)
        ]