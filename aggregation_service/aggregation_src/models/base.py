from sqlalchemy.orm import declarative_base

"""
Base class for all ORM services.

ALl the existing or future models should inherit from this class.
SQLAlchemy uses this to:

    1. Map Python classes to database tables.
    2. Collect metadata (tables, columns, relationships, etc.)
    3. Schema Generation.
"""
Base = declarative_base()