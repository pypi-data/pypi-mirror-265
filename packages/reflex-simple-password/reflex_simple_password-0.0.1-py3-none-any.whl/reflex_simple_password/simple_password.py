"""Reflex custom component SimplePassword."""

from typing import ClassVar
import reflex as rx
import os

PASSWORD = os.getenv("PASSWORD")

class SimplePasswordState(rx.State):
    """A simple password component with state."""

    if not os.getenv("PASSWORD"):
        raise Exception("PASSWORD environment variable is not set.")

    password: str = ""

    correct_password: bool = False

    login_route: ClassVar[str]

    redirect_route: ClassVar[str]

    def check_login(self):
        """Check if a user is logged in."""
        if not self.logged_in:
            return rx.redirect(SimplePasswordState.login_route)

    @rx.var
    def logged_in(self):
        """Check if a user is logged in."""
        return self.correct_password

    def check_password(self):
        if PASSWORD == self.password:
            self.correct_password = True
            return rx.redirect(SimplePasswordState.redirect_route)
        else:
            return rx.window_alert("Invalid password.")



def simple_password(size="3", **props):
    return rx.vstack(
        rx.input(
            type="password",
            placeholder="Password",
            on_blur=SimplePasswordState.set_password,
            size=size,
        ),
        rx.button(
            "Log in", on_click=SimplePasswordState.check_password, size=size,
        ),
        align=props.pop("align", "center"),
        spacing=props.pop("spacing", "4"),
        **props,
    )


def require_login(page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:
    """Decorator to require authentication before rendering a page.

    If the user is not authenticated, then redirect to the login page.

    Args:
        page: The page to wrap.

    Returns:
        The wrapped page component.
    """

    def protected_page():
        return rx.fragment(
            rx.cond(
                SimplePasswordState.is_hydrated & SimplePasswordState.logged_in,
                page(),
                rx.center(
                    # When this text mounts, it will redirect to the login page
                    rx.text("Loading...", on_mount=SimplePasswordState.check_login),
                ),
            )
        )

    protected_page.__name__ = page.__name__
    return protected_page