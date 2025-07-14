from nicegui import ui
from app.counter_service import get_counter_value, increment_counter, reset_counter


def create():
    """Create counter UI components and register pages."""

    @ui.page("/")
    def counter_page():
        # Apply modern theme colors
        ui.colors(
            primary="#2563eb",
            secondary="#64748b",
            accent="#10b981",
            positive="#10b981",
            negative="#ef4444",
            warning="#f59e0b",
            info="#3b82f6",
        )

        # Main container with modern styling
        with ui.column().classes("w-full max-w-md mx-auto mt-12 p-8"):
            # App title
            ui.label("Simple Counter").classes("text-3xl font-bold text-center text-gray-800 mb-8")

            # Counter display card
            with ui.card().classes("p-8 bg-white shadow-lg rounded-xl text-center mb-6"):
                counter_display = ui.label().classes("text-6xl font-bold text-primary mb-2")
                ui.label("Current Count").classes("text-sm text-gray-500 uppercase tracking-wider")

                # Initialize counter display
                initial_value = get_counter_value("main")
                counter_display.text = str(initial_value)

            # Action buttons
            with ui.row().classes("gap-4 justify-center w-full"):
                # Increment button
                def handle_increment():
                    new_value = increment_counter("main")
                    counter_display.text = str(new_value)
                    ui.notify(f"Counter incremented to {new_value}!", type="positive")

                ui.button("Increment", on_click=handle_increment).classes(
                    "bg-primary text-white px-6 py-3 rounded-lg shadow-md hover:shadow-lg transition-shadow font-medium"
                )

                # Reset button
                def handle_reset():
                    new_value = reset_counter("main")
                    counter_display.text = str(new_value)
                    ui.notify("Counter reset to 0!", type="info")

                ui.button("Reset", on_click=handle_reset).classes(
                    "bg-gray-500 text-white px-6 py-3 rounded-lg shadow-md hover:shadow-lg "
                    "transition-shadow font-medium"
                )

            # Info section
            with ui.card().classes("mt-8 p-4 bg-gray-50 rounded-lg"):
                ui.label("ℹ️ About").classes("text-sm font-semibold text-gray-700 mb-2")
                ui.label(
                    "This counter value is persisted in PostgreSQL database and will "
                    "retain its value across application restarts."
                ).classes("text-xs text-gray-600 leading-relaxed")
