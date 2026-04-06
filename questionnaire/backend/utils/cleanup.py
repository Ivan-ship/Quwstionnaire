from models.user_models import PendingUser, ResetPassword
from routers.database import SessionLocal
from datetime import datetime, timedelta

def clean_pending_users():
    db = SessionLocal()
    expire_time = datetime.utcnow() - timedelta(minutes = 5)

    db.query(PendingUser).filter(PendingUser.created_at < expire_time).delete(synchronize_session=False)

    db.commit()
    db.close()

def clean_reset_password():
    db = SessionLocal()
    expire_time = datetime.utcnow() - timedelta(minutes = 5)
    db.query(ResetPassword).filter(ResetPassword.created_at < expire_time).delete(synchronize_session=False)
    db.commit()
    db.close()