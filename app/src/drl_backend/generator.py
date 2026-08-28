"""Create synthetic events and submit them through the ingestion API."""

import argparse
import json
from datetime import UTC, datetime
from urllib.request import Request, urlopen
from uuid import uuid4

from .events import Event


def create_synthetic_event() -> Event:
    """Create one valid temperature-reading event for local flow verification."""
    return Event(
        event_id=uuid4(),
        event_type=" Temperature_Reading ",
        created_at=datetime.now(UTC),
        payload={"temperature_c": 21.5},
    )


def send_event(api_url: str, event: Event) -> dict[str, str]:
    """Submit an event to the ingestion API and return its acceptance response."""
    request = Request(
        url=f"{api_url.rstrip('/')}/events",
        data=json.dumps(event.model_dump(mode="json")).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request) as response:
        if response.status != 202:
            raise RuntimeError(f"Ingestion API returned unexpected status {response.status}")

        return json.load(response)


def main() -> None:
    """Generate and submit one event to a local ingestion API."""
    parser = argparse.ArgumentParser(
        description="Send one synthetic event to the ingestion API."
    )
    parser.add_argument(
        "--api-url",
        default="http://127.0.0.1:8000",
        help="Base URL for the ingestion API (default: %(default)s)",
    )
    args = parser.parse_args()

    event = create_synthetic_event()
    response = send_event(args.api_url, event)
    print(json.dumps({"event_id": str(event.event_id), "response": response}))


if __name__ == "__main__":
    main()
