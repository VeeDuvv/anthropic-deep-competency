"""Tests for task CRUD endpoints."""


def test_create_task(client, auth_headers, sample_project):
    response = client.post(
        "/api/projects/test-project/tasks/",
        json={"title": "Fix the bug", "priority": "high"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Fix the bug"
    assert data["priority"] == "high"
    assert data["status"] == "todo"


def test_list_tasks(client, auth_headers, sample_project):
    # Create two tasks
    client.post(
        "/api/projects/test-project/tasks/",
        json={"title": "Task 1"},
        headers=auth_headers,
    )
    client.post(
        "/api/projects/test-project/tasks/",
        json={"title": "Task 2"},
        headers=auth_headers,
    )

    response = client.get("/api/projects/test-project/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_task_status(client, auth_headers, sample_project):
    create_resp = client.post(
        "/api/projects/test-project/tasks/",
        json={"title": "Task to complete"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]

    response = client.patch(
        f"/api/projects/test-project/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "done"
    assert response.json()["completed_at"] is not None


def test_filter_tasks_by_status(client, auth_headers, sample_project):
    client.post(
        "/api/projects/test-project/tasks/",
        json={"title": "Todo task"},
        headers=auth_headers,
    )
    create_resp = client.post(
        "/api/projects/test-project/tasks/",
        json={"title": "Done task"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]
    client.patch(
        f"/api/projects/test-project/tasks/{task_id}",
        json={"status": "done"},
        headers=auth_headers,
    )

    response = client.get(
        "/api/projects/test-project/tasks/?status=todo", headers=auth_headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Todo task"


def test_delete_task(client, auth_headers, sample_project):
    create_resp = client.post(
        "/api/projects/test-project/tasks/",
        json={"title": "Delete me"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]

    response = client.delete(
        f"/api/projects/test-project/tasks/{task_id}", headers=auth_headers
    )
    assert response.status_code == 204


def test_task_not_found(client, auth_headers, sample_project):
    response = client.get("/api/projects/test-project/tasks/9999", headers=auth_headers)
    assert response.status_code == 404
