import json
from io import BytesIO

from drl_backend import generator


def test_create_synthetic_event_returns_a_valid_temperature_event() -> None:
    event = generator.create_synthetic_event()

    assert event.event_type == " Temperature_Reading "
    assert event.created_at.tzinfo is not None
    assert event.payload == {"temperature_c": 21.5}


def test_send_event_posts_event_to_ingestion_api(monkeypatch) -> None:
    captured_request = {}

    class AcceptedResponse(BytesIO):
        status = 202

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback) -> None:
            self.close()

    def fake_urlopen(request):
        captured_request["request"] = request
        return AcceptedResponse(
            b'{"status": "accepted", "event_id": "123e4567-e89b-12d3-a456-426614174000"}'
        )

    event = generator.create_synthetic_event()
    monkeypatch.setattr(generator, "urlopen", fake_urlopen)

    response = generator.send_event("http://localhost:8000/", event)

    request = captured_request["request"]
    assert request.full_url == "http://localhost:8000/events"
    assert request.get_method() == "POST"
    assert request.get_header("Content-type") == "application/json"
    assert json.loads(request.data) == event.model_dump(mode="json")
    assert response == {
        "status": "accepted",
        "event_id": "123e4567-e89b-12d3-a456-426614174000",
    }
