import pytest
from app.counter_service import get_or_create_counter, get_counter_value, increment_counter, reset_counter
from app.database import reset_db


@pytest.fixture()
def new_db():
    reset_db()
    yield
    reset_db()


def test_get_or_create_counter_new(new_db):
    """Test creating a new counter."""
    counter = get_or_create_counter("test_counter")

    assert counter.name == "test_counter"
    assert counter.value == 0
    assert counter.id is not None


def test_get_or_create_counter_existing(new_db):
    """Test retrieving an existing counter."""
    # Create first counter
    counter1 = get_or_create_counter("existing_counter")
    counter1_id = counter1.id

    # Get the same counter again
    counter2 = get_or_create_counter("existing_counter")

    assert counter2.id == counter1_id
    assert counter2.name == "existing_counter"
    assert counter2.value == 0


def test_get_counter_value_new(new_db):
    """Test getting value from new counter."""
    value = get_counter_value("new_counter")
    assert value == 0


def test_get_counter_value_existing(new_db):
    """Test getting value from existing counter."""
    # Create and increment counter
    increment_counter("existing_counter")
    increment_counter("existing_counter")

    value = get_counter_value("existing_counter")
    assert value == 2


def test_increment_counter_new(new_db):
    """Test incrementing a new counter."""
    value = increment_counter("new_counter")
    assert value == 1


def test_increment_counter_existing(new_db):
    """Test incrementing an existing counter."""
    # Create counter and increment once
    increment_counter("test_counter")

    # Increment again
    value = increment_counter("test_counter")
    assert value == 2


def test_increment_counter_multiple_times(new_db):
    """Test incrementing counter multiple times."""
    counter_name = "multi_increment"

    # Increment 5 times
    for i in range(1, 6):
        value = increment_counter(counter_name)
        assert value == i

    # Verify final value
    final_value = get_counter_value(counter_name)
    assert final_value == 5


def test_reset_counter_new(new_db):
    """Test resetting a new counter."""
    value = reset_counter("new_counter")
    assert value == 0


def test_reset_counter_existing(new_db):
    """Test resetting an existing counter."""
    # Create and increment counter
    increment_counter("test_counter")
    increment_counter("test_counter")
    increment_counter("test_counter")

    # Reset counter
    value = reset_counter("test_counter")
    assert value == 0

    # Verify reset persisted
    current_value = get_counter_value("test_counter")
    assert current_value == 0


def test_multiple_counters(new_db):
    """Test managing multiple independent counters."""
    # Create and increment different counters
    increment_counter("counter_a")
    increment_counter("counter_a")
    increment_counter("counter_b")

    # Verify they're independent
    assert get_counter_value("counter_a") == 2
    assert get_counter_value("counter_b") == 1

    # Reset one counter
    reset_counter("counter_a")

    # Verify only one was reset
    assert get_counter_value("counter_a") == 0
    assert get_counter_value("counter_b") == 1


def test_counter_persistence_across_operations(new_db):
    """Test that counter values persist across different operations."""
    counter_name = "persistence_test"

    # Initial increment
    value1 = increment_counter(counter_name)
    assert value1 == 1

    # Get value (should be same)
    value2 = get_counter_value(counter_name)
    assert value2 == 1

    # Increment again
    value3 = increment_counter(counter_name)
    assert value3 == 2

    # Reset
    value4 = reset_counter(counter_name)
    assert value4 == 0

    # Increment after reset
    value5 = increment_counter(counter_name)
    assert value5 == 1


def test_counter_name_uniqueness(new_db):
    """Test that counter names are unique and case-sensitive."""
    increment_counter("TestCounter")
    increment_counter("testcounter")
    increment_counter("TESTCOUNTER")

    # All should be different counters
    assert get_counter_value("TestCounter") == 1
    assert get_counter_value("testcounter") == 1
    assert get_counter_value("TESTCOUNTER") == 1


def test_counter_updated_at_field(new_db):
    """Test that updated_at field is properly maintained."""
    counter1 = get_or_create_counter("timestamp_test")
    original_updated_at = counter1.updated_at

    # Increment counter
    increment_counter("timestamp_test")

    # Get updated counter
    counter2 = get_or_create_counter("timestamp_test")

    # updated_at should be different (newer)
    assert counter2.updated_at > original_updated_at
