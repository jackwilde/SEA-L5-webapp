from sqlalchemy import Integer, String, Text, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase
from flask_login import UserMixin


class Base(DeclarativeBase):
    pass


class User(Base, UserMixin):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(120), nullable=False)
    first_name = mapped_column(String(20), nullable=False)
    last_name = mapped_column(String(20), nullable=False)
    password = mapped_column(Text, nullable=False)
    admin = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"user_id: {self.id}, email={self.email}"


class Training(Base):
    __tablename__ = "training"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    course_name = mapped_column(String(120), nullable=False)
    category_id = mapped_column(ForeignKey("training_categories.id"),
                                    nullable=False)
    date_completed = mapped_column(Date, nullable=False)
    certification = mapped_column(Boolean)

class TrainingCategory(Base):
    __tablename__ = "training_categories"
    id = mapped_column(Integer, primary_key=True)
    category_name = mapped_column(String(60), nullable=False)

    def __repr__(self):
        return self.category_name

