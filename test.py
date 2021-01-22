import os
import json
import pytest
import app

JWT_SUPER_USER = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFUUllhVDYtVDhHbnlUMXJYWTFnMSJ9.eyJpc3MiOiJodHRwczovL2FqYWppLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTMzMjFkMzkxOWJjMDA3NmEzOTlhMyIsImF1ZCI6IlBsYXl0aW1lLVRyYWNrZXIiLCJpYXQiOjE2MTEyNjg0MTAsImV4cCI6MTYxMTM1NDgxMCwiYXpwIjoiMEk3NktGSTZ3QUlQRVdrMEYzeHdNNjJiS1NUWVB1c3UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwbGF5dGltZSIsImdldDptb3N0LXBsYXl0aW1lIiwiZ2V0OnBsYXl0aW1lL2lkIiwiZ2V0OnBsYXl0aW1lcyIsInBhdGNoOnBsYXl0aW1lIiwicG9zdDpwbGF5dGltZSJdfQ.W2eLuYzs-QXTjV2Vu2U2f2EsbIVDDL4j12zOD_g3p73S6-Wprq7MLlpBACjxvSE8n9yTP2PK41AfkLnftwnuIGe6rmb25FVNmEyuS3XKaEXPpz0kDqI6t1byJICoHOUt_vqGPlFZyXGCf0MotNcW0mYR8UKXnekjFKTkyWBVId7k5FurCuXkqRYHcXogzzGxY8vTeZ_ECIRF29ucaEnQPiwGEYgs7h9DhRJ88COxHj_kT15mLh8uug0mcTKrE-6OnwrbtRQV-82y5PRURrd4iodFp86lfbuAuke3PdMIYoUSF6EH7ff6NhhpG1bcyVkspkZnZ90FzZiWE5r7a6eD_A"
JWT_NOT_SO_SUPER_USER = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFUUllhVDYtVDhHbnlUMXJYWTFnMSJ9.eyJpc3MiOiJodHRwczovL2FqYWppLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTMzMjFkMzkxOWJjMDA3NmEzOTlhMyIsImF1ZCI6IlBsYXl0aW1lLVRyYWNrZXIiLCJpYXQiOjE2MTEyNjg4MTQsImV4cCI6MTYxMTM1NTIxNCwiYXpwIjoiMEk3NktGSTZ3QUlQRVdrMEYzeHdNNjJiS1NUWVB1c3UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDptb3N0LXBsYXl0aW1lIiwiZ2V0OnBsYXl0aW1lL2lkIiwiZ2V0OnBsYXl0aW1lcyJdfQ.BkLBCmU9cQWrZ6bcfT1M6jUa7dogPJRUMvqp1jq0fKcrWBGoErBBacpTUoohdiazJg4gBKMSd4C38LRJHpaKitnlT5YXDtlvZlTW0jiPAkSRETu5uHUAAZrxE_6gccnbPpBFmzRxnm5AhWOKZsXIN8QVln5j5T5tinTlA1Aks6kdy0lX-c0aU_JMWRy_AgdiAKVPo_MovB4qsHtHQdcAg1mZfFf3xt4yXFc9eh2A7XNmxS3zoQv5zFydnM0fHLNQflsNghN_Dt-cgxYkbXEBPM6eLjUiW6f_2EdnDDx7Xa22paxrs7xeTdGSgt-Z9DaPEXfGpbpE3jvZm1LlNFQ1Ew"

PLAYTIME_ID = 0
PLAYER_ID = 0


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    yield client


def test_post_playtime(client):
    body = {
        "game": "Overwatch",
        "player": "Abdullah",
        "playtime": "23:40",
        "genre": "Shooter"
    }
    header = {
        'Authorization': 'Bearer {}'.format(JWT_SUPER_USER)
    }

    response = client.post('/playtime', headers=header, json=body)

    returned = json.loads(response.data)
    global PLAYTIME_ID
    PLAYTIME_ID = returned['Game Added']['playtime_id']
    global PLAYER_ID
    PLAYER_ID = returned['Game Added']['player_id']
    assert response.status_code == 200


def test_get_playtime(client):
    header = {
        'Authorization': 'Bearer {}'.format(JWT_NOT_SO_SUPER_USER)
    }
    response = client.get('/playtime/{}'.format(PLAYER_ID), headers=header)
    assert response.status_code == 200


def test_get_most_playtime(client):
    header = {
        'Authorization': 'Bearer {}'.format(JWT_SUPER_USER)
    }
    response = client.get('/most-playtime'.format(PLAYER_ID), headers=header)
    
    assert response.status_code == 200
def test_get_all_playtimes(client):
    header = {
        'Authorization': 'Bearer {}'.format(JWT_SUPER_USER)
    }
    response = client.get('/playtimes', headers=header)
    assert response.status_code == 200


def test_403_unauthorized(client):
    body = {
        "game": "Overwatch",
        "player": "Abdullah",
        "playtime": "23:40",
        "genre": "Shooter"
    }
    header = {
        'Authorization': 'Bearer {}'.format(JWT_NOT_SO_SUPER_USER)
    }
    response = client.post('/playtime', headers=header, json=body)
    assert response.status_code == 403


def test_patch_playtime(client):
    body = {
        "game": "Fifa",
        "playtime": "23:40",
        "genre": "Shooter"
    }
    header = {
        'Authorization': 'Bearer {}'.format(JWT_SUPER_USER)
    }
    print(PLAYTIME_ID)
    response = client.patch(
        '/playtime/{}'.format(PLAYTIME_ID), headers=header, json=body)
    assert response.status_code == 200


def test_delete_playtime(client):
    header = {
        'Authorization': 'Bearer {}'.format(JWT_SUPER_USER)
    }
    print(PLAYTIME_ID)
    response = client.delete(
        '/playtime/{}'.format(PLAYTIME_ID), headers=header)
    assert response.status_code == 200
