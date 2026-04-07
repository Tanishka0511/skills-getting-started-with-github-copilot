from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app, follow_redirects=False)


def test_get_activities():
    """Test GET /activities returns all activities with correct structure."""
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    # Check that some expected activities exist
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Soccer Club", "Art Club", "Drama Club", "Debate Club", "Science Club"
    ]
    for activity in expected_activities:
        assert activity in data

    # Check structure of one activity
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_signup_success():
    """Test successful signup for an activity."""
    response = client.post("/activities/Chess Club/signup?email=test@example.com")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Signed up test@example.com for Chess Club"

    # Verify participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]


def test_signup_duplicate():
    """Test that duplicate signup is prevented."""
    # First signup
    client.post("/activities/Programming Class/signup?email=duplicate@example.com")

    # Attempt duplicate signup
    response = client.post("/activities/Programming Class/signup?email=duplicate@example.com")
    assert response.status_code == 400

    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_delete_participant():
    """Test removing a participant from an activity."""
    # Add participant first
    client.post("/activities/Gym Class/signup?email=delete@example.com")

    # Remove participant
    response = client.delete("/activities/Gym Class/participants/delete@example.com")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Removed delete@example.com from Gym Class"

    # Verify participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "delete@example.com" not in data["Gym Class"]["participants"]


def test_delete_nonexistent_participant():
    """Test deleting a participant who is not signed up."""
    response = client.delete("/activities/Basketball Team/participants/nonexistent@example.com")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data


def test_signup_invalid_activity():
    """Test signup for non-existent activity."""
    response = client.post("/activities/Invalid Activity/signup?email=test@example.com")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data


def test_delete_invalid_activity():
    """Test deleting participant from non-existent activity."""
    response = client.delete("/activities/Invalid Activity/participants/test@example.com")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data


def test_root_redirect():
    """Test that root path redirects to static index.html."""
    response = client.get("/")
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"