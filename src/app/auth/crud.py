from sqlalchemy.orm import Session

from .models import Verification


class CRUDVerify:
    def get(self, db: Session, uuid: str) -> Verification:
        return db.query(
            Verification
        ).filter(Verification.link == uuid).first()

    def create(self, db: Session, user: int) -> Verification:
        db_obj = Verification(user_id=user)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, uuid: str) -> Verification:
        obj = db.query(
            Verification
        ).filter(Verification.link == uuid).first()
        db.delete(obj)
        db.commit()
        return obj


auth_verify = CRUDVerify()
