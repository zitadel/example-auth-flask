# file: lib/guard.py
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from flask import Response, g, redirect, request, session, url_for

F = TypeVar("F", bound=Callable[..., Any])


def require_auth(view: F) -> F:
    """
    Middleware that ensures the user is authenticated before accessing
    protected routes. It retrieves the current session and validates that a
    user is present. If authentication fails, the client is redirected to
    the sign-in page with the original URL preserved in the callbackUrl
    query parameter. On success, the session is attached to `g.auth_session`
    and control is passed to the next handler.

    - Must be used after session middleware so that request cookies and body
      are parsed.
    - Redirects unauthenticated users to
      `/auth/signin?callbackUrl=<original URL>`.
    - Original request URL is URL-encoded in callbackUrl.

    Example
    -------

    from lib.guard import require_auth

    @app.route("/profile")
    @require_auth
    def profile():
        return "protected"
    """

    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any) -> Response:
        auth_session = session.get("auth_session")

        if not auth_session or not auth_session.get("user"):
            callback_url = request.url
            return cast(
                Response,
                redirect(url_for("auth.signin", callbackUrl=callback_url, _external=False)),
            )

        g.auth_session = auth_session
        return cast(Response, view(*args, **kwargs))

    return cast(F, wrapped)
