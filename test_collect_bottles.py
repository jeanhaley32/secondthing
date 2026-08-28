"""Unit tests for /collect-bottles — run with `pytest`, no live server needed."""

from fastapi.testclient import TestClient

from app import app, MAX_COORD

client = TestClient(app)


def _bottle(char, x, y):
    return {"character": char, "coordinates": {"x": x, "y": y}}


def test_valid_message_is_assembled():
    resp = client.post("/collect-bottles", json=[_bottle("H", 0, 0), _bottle("i", 1, 0)])
    assert resp.status_code == 200
    body = resp.json()
    assert body["message"] == "Hi"
    assert body["bottles_processed"] == 2


def test_empty_list_returns_400_not_500():
    # The "No bottles provided" 400 must reach the client as a 400, not be
    # swallowed by the generic handler and re-wrapped as a 500.
    resp = client.post("/collect-bottles", json=[])
    assert resp.status_code == 400
    assert "No bottles" in resp.json()["detail"]


def test_oversized_coordinate_is_rejected():
    # Regression: an unbounded coordinate used to size the grid could OOM the
    # pod. It must be rejected as a 400 before any grid allocation.
    resp = client.post("/collect-bottles", json=[_bottle("X", 10**9, 10**9)])
    assert resp.status_code == 400
    assert str(MAX_COORD) in resp.json()["detail"]


def test_negative_coordinate_is_rejected():
    resp = client.post("/collect-bottles", json=[_bottle("X", -1, 0)])
    assert resp.status_code == 400


def test_boundary_coordinate_is_allowed():
    resp = client.post("/collect-bottles", json=[_bottle("X", MAX_COORD, 0)])
    assert resp.status_code == 200
