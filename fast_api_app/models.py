from database import Base
from sqlalchemy import Column, Integer, String, Text


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String, unique=True, index=True)
    views_count = Column(Integer, default=0, index=True)
    cooking_time_minutes = Column(Integer, index=True)
    ingredients = Column(Text)
    description = Column(Text)
