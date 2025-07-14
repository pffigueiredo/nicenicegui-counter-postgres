import pytest
from nicegui.testing import User
from app.database import reset_db
from app.counter_service import increment_counter


@pytest.fixture()
def new_db():
    reset_db()
    yield
    reset_db()


async def test_counter_page_loads(user: User, new_db) -> None:
    """Test that the counter page loads correctly."""
    await user.open("/")

    # Check page title
    await user.should_see("Simple Counter")

    # Check counter display shows initial value
    await user.should_see("Current Count")
    await user.should_see("0")

    # Check buttons are present
    await user.should_see("Increment")
    await user.should_see("Reset")


async def test_counter_increment_functionality(user: User, new_db) -> None:
    """Test counter increment functionality."""
    await user.open("/")

    # Initial state should show 0
    await user.should_see("0")

    # Click increment button
    user.find("Increment").click()

    # Should show 1
    await user.should_see("1")

    # Click increment again
    user.find("Increment").click()

    # Should show 2
    await user.should_see("2")


async def test_counter_reset_functionality(user: User, new_db) -> None:
    """Test counter reset functionality."""
    await user.open("/")

    # Increment counter a few times
    user.find("Increment").click()
    user.find("Increment").click()
    user.find("Increment").click()

    # Should show 3
    await user.should_see("3")

    # Click reset button
    user.find("Reset").click()

    # Should show 0
    await user.should_see("0")


async def test_counter_persistence_across_page_loads(user: User, new_db) -> None:
    """Test that counter value persists across page reloads."""
    await user.open("/")

    # Increment counter
    user.find("Increment").click()
    user.find("Increment").click()

    # Should show 2
    await user.should_see("2")

    # Reload page
    await user.open("/")

    # Should still show 2
    await user.should_see("2")


async def test_counter_with_existing_database_value(user: User, new_db) -> None:
    """Test that counter loads existing value from database."""
    # Pre-populate database with counter value
    increment_counter("main")
    increment_counter("main")
    increment_counter("main")

    # Load page
    await user.open("/")

    # Should show the existing value
    await user.should_see("3")

    # Increment should work correctly
    user.find("Increment").click()
    await user.should_see("4")


async def test_counter_notifications(user: User, new_db) -> None:
    """Test that increment and reset show notifications."""
    await user.open("/")

    # Click increment - should show success notification
    user.find("Increment").click()
    await user.should_see("Counter incremented to 1!")

    # Click reset - should show info notification
    user.find("Reset").click()
    await user.should_see("Counter reset to 0!")


async def test_counter_ui_elements_styling(user: User, new_db) -> None:
    """Test that UI elements are properly styled and accessible."""
    await user.open("/")

    # Check that buttons exist and can be found
    increment_button = user.find("Increment")
    reset_button = user.find("Reset")

    # Should be able to interact with buttons
    increment_button.click()
    await user.should_see("1")

    reset_button.click()
    await user.should_see("0")


async def test_counter_info_section(user: User, new_db) -> None:
    """Test that info section displays correctly."""
    await user.open("/")

    # Check info section content
    await user.should_see("About")
    await user.should_see("This counter value is persisted in PostgreSQL database")
    await user.should_see("retain its value across application restarts")
