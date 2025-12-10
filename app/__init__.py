from typing import Any, Dict, Optional

from flask import Flask, render_template, url_for

from lib.auth import get_session, register_auth_routes
from lib.config import config
from lib.guard import require_auth


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = config.SESSION_SECRET

    register_auth_routes(app)

    @app.route("/")
    def home() -> Any:
        session_data: Optional[Dict[str, Any]] = get_session()
        return render_template(
            "index.html",
            isAuthenticated=bool(session_data),
            loginUrl=url_for("auth.signin_zitadel"),
        )

    @app.route("/profile")
    @require_auth
    def profile() -> Any:
        session_data: Dict[str, Any] = get_session()  # type: ignore[assignment]
        return render_template("profile.html", userJson=session_data["user"])

    @app.errorhandler(404)
    def not_found(_: Any) -> Any:
        return render_template("not-found.html"), 404

    return app
