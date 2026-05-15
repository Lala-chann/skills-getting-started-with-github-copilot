import src.app as app_module


def test_get_activities_returns_all_activities(client_fixture):
    # Arrange (none)
    # Act
    resp = client_fixture.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client_fixture):
    # Arrange
    activity = "Basketball Team"
    email = "newstudent@mergington.edu"
    if email in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].remove(email)

    # Act
    resp = client_fixture.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]
    assert resp.json() == {"message": f"Signed up {email} for {activity}"}

    # Cleanup
    app_module.activities[activity]["participants"].remove(email)


def test_duplicate_signup_is_rejected(client_fixture):
    # Arrange
    activity = "Basketball Team"
    email = "duplicate@mergington.edu"
    if email not in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].append(email)

    # Act
    resp = client_fixture.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 400


def test_remove_participant_unregisters_student(client_fixture):
    # Arrange
    activity = "Basketball Team"
    email = "remove_me@mergington.edu"
    if email not in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].append(email)

    # Act
    resp = client_fixture.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_remove_missing_participant_returns_404(client_fixture):
    # Arrange
    activity = "Basketball Team"
    email = "noone@mergington.edu"
    if email in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].remove(email)

    # Act
    resp = client_fixture.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
