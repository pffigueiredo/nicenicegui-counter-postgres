from datetime import datetime
from sqlmodel import select

from app.database import get_session
from app.models import Counter


def get_or_create_counter(name: str) -> Counter:
    """Get existing counter or create a new one with the given name."""
    with get_session() as session:
        # Try to find existing counter
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is None:
            # Create new counter
            counter = Counter(name=name, value=0)
            session.add(counter)
            session.commit()
            session.refresh(counter)

        return counter


def get_counter_value(name: str) -> int:
    """Get current counter value."""
    counter = get_or_create_counter(name)
    return counter.value


def increment_counter(name: str) -> int:
    """Increment counter value by 1 and return new value."""
    with get_session() as session:
        # Get the counter
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is None:
            counter = Counter(name=name, value=1)
            session.add(counter)
        else:
            counter.value += 1
            counter.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(counter)
        return counter.value


def reset_counter(name: str) -> int:
    """Reset counter value to 0 and return new value."""
    with get_session() as session:
        statement = select(Counter).where(Counter.name == name)
        counter = session.exec(statement).first()

        if counter is None:
            counter = Counter(name=name, value=0)
            session.add(counter)
        else:
            counter.value = 0
            counter.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(counter)
        return counter.value
