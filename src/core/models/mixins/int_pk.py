from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class IntPkMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
