# Third-party
import argparse
import logging
from flask import jsonify, send_file
from flask_socketio import SocketIO  # type: ignore

# Glow
from glow.api.app import glow_api

# Endpoint modules need to be imported for endpoints
# to be registered.
import glow.api.endpoints.runs  # noqa: F401
import glow.api.endpoints.edges  # noqa: F401
import glow.api.endpoints.artifacts  # noqa: F401
from glow.config import DEFAULT_ENV, get_config, switch_env  # noqa: F401


@glow_api.route("/")
@glow_api.route("/<path:path>")
def index(path=""):
    """
    Returns the index page of the UI app.

    To build the UI app:
    $ cd ui
    $ npm run build
    """
    return send_file("../ui/build/index.html")


@glow_api.route("/api/v1/ping")
def ping():
    """
    Basic health ping. Does not include DB liveness check.
    """
    return jsonify({"status": "ok"})


socketio = SocketIO(glow_api)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Sematic API server")
    parser.add_argument("--env", required=False, default=DEFAULT_ENV, type=str)
    parser.add_argument(
        "--port", required=False, default=get_config().api_port, type=int
    )
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    args = parse_arguments()
    switch_env(args.env)

    glow_api.debug = True
    # glow_api.run(debug=True)

    socketio.run(glow_api, port=args.port)
