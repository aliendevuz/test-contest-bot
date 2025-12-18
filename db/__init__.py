import os
from db.sqlite_impl import SqliteUserRepo


def _sqlite_path_from_url(url: str) -> str:
    # accept formats like sqlite:///./data.db or sqlite:////absolute/path.db
    if url.startswith("sqlite://"):
        # strip scheme: sqlite:/// leaves /// so we remove that
        path = url.replace("sqlite:///", "")
        # Handle relative paths with ./
        if path.startswith("./"):
            path = path[2:]
        # Make relative paths absolute using current working directory
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)
        return path
    return url


def get_user_repo(database_url: str):
    if database_url.startswith("sqlite"):
        path = _sqlite_path_from_url(database_url)
        return SqliteUserRepo(path)
    raise RuntimeError("Only sqlite backend implemented in this example")
