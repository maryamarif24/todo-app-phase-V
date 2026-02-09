"""
Tag service for the Todo application with advanced features.

This module provides CRUD operations for the Tag model.
"""

from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..models.tag import Tag


def create_tag(*, session: Session, name: str, user_id: str, color: str = "#3B82F6") -> Optional[Tag]:
    """
    Create a new tag for the specified user.

    Args:
        session: Database session
        name: Name of the tag
        user_id: ID of the user creating the tag
        color: Color for the tag (hex format, defaults to blue)

    Returns:
        The created Tag object if successful, None if a tag with the same name already exists for the user
    """
    # Check if tag already exists for this user
    existing_tag = get_tag_by_name(session=session, name=name, user_id=user_id)
    if existing_tag:
        return existing_tag  # Return existing tag if it exists

    # Create the tag object
    tag = Tag(name=name, user_id=user_id, color=color)

    # Add to database
    try:
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag
    except IntegrityError:
        # Handle potential integrity errors
        session.rollback()
        return None


def get_tag_by_name(*, session: Session, name: str, user_id: str) -> Optional[Tag]:
    """
    Get a tag by its name for the specified user.

    Args:
        session: Database session
        name: Name of the tag to retrieve
        user_id: ID of the user who owns the tag

    Returns:
        The Tag object if found and owned by the user, None otherwise
    """
    statement = select(Tag).where(Tag.name == name, Tag.user_id == user_id)
    tag = session.exec(statement).first()
    return tag


def get_tags_by_user(*, session: Session, user_id: str) -> List[Tag]:
    """
    Get all tags for the specified user.

    Args:
        session: Database session
        user_id: ID of the user whose tags to retrieve

    Returns:
        List of tags belonging to the user
    """
    statement = select(Tag).where(Tag.user_id == user_id)
    tags = session.exec(statement).all()
    return tags