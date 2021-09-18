from src.app.base.crud_base import CRUDBase
from .models import Verification
from .schemas import VerificationCreate


class CRUDVerify(CRUDBase[Verification,
                          VerificationCreate, VerificationCreate]):
    pass


auth_verify = CRUDVerify(Verification)
