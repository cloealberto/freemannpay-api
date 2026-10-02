import os
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import Float, Integer, String, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

security = HTTPBearer()

VALID_TOKEN = os.getenv("PAYMENT_API_TOKEN")
if VALID_TOKEN is None or not VALID_TOKEN.strip():
    raise RuntimeError(
        "PAYMENT_API_TOKEN environment variable is not set or is empty."
    )
VALID_TOKEN = VALID_TOKEN.strip()


def required_environment_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"{name} environment variable is not set or is empty.")
    return value.strip()


database_url = URL.create(
    drivername="postgresql+psycopg",
    username=required_environment_variable("POSTGRES_USER"),
    password=required_environment_variable("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    database=required_environment_variable("POSTGRES_DB"),
)
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class PaymentRecord(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    method: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FreemannPay | Payment Simulation API",
    lifespan=lifespan,
)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifica se o token enviado no Header (Bearer) é válido.
    Se não for, a API barra a requisição com erro 401.
    """
    if credentials.credentials != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return credentials.credentials


def get_db():
    with SessionLocal() as db:
        yield db


def serialize_payment(payment: PaymentRecord) -> dict:
    return {
        "id": payment.id,
        "user_id": payment.user_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "method": payment.method,
        "status": payment.status,
    }

class PaymentPayload(BaseModel):
    user_id: int
    amount: float
    currency: str
    method: str  # CREDIT_CARD, PIX, or BOLETO

@app.post("/payments", status_code=201, dependencies=[Depends(verify_token)])
def create_payment(payment: PaymentPayload, db: Session = Depends(get_db)):
    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    payment_id = str(uuid.uuid4())
    new_payment = PaymentRecord(
        id=payment_id,
        user_id=payment.user_id,
        amount=payment.amount,
        currency=payment.currency,
        method=payment.method,
        status="PENDING",
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return serialize_payment(new_payment)

@app.get("/payments/{payment_id}", dependencies=[Depends(verify_token)])
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.get(PaymentRecord, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return serialize_payment(payment)