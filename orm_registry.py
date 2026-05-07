"""Register all SQLAlchemy models on ``Base.metadata`` (``app.models`` package ``__init__`` is empty)."""


def import_all_models() -> None:
    import app.models.activity_logs  # noqa: F401
    import app.models.codes  # noqa: F401
    import app.models.meetings  # noqa: F401
    import app.models.notifications  # noqa: F401
    import app.models.permissions  # noqa: F401
    import app.models.profiles  # noqa: F401
    import app.models.role_permissions  # noqa: F401
    import app.models.roles  # noqa: F401
    import app.models.team_roles  # noqa: F401
    import app.models.user_roles  # noqa: F401
    import app.models.users  # noqa: F401
