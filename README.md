# Playtime Tracker

This is an app to track your game playtime

# Users

## super user:

```bash
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFUUllhVDYtVDhHbnlUMXJYWTFnMSJ9.eyJpc3MiOiJodHRwczovL2FqYWppLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTMzMjFkMzkxOWJjMDA3NmEzOTlhMyIsImF1ZCI6IlBsYXl0aW1lLVRyYWNrZXIiLCJpYXQiOjE2MTEyNjg0MTAsImV4cCI6MTYxMTM1NDgxMCwiYXpwIjoiMEk3NktGSTZ3QUlQRVdrMEYzeHdNNjJiS1NUWVB1c3UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwbGF5dGltZSIsImdldDptb3N0LXBsYXl0aW1lIiwiZ2V0OnBsYXl0aW1lL2lkIiwiZ2V0OnBsYXl0aW1lcyIsInBhdGNoOnBsYXl0aW1lIiwicG9zdDpwbGF5dGltZSJdfQ.W2eLuYzs-QXTjV2Vu2U2f2EsbIVDDL4j12zOD_g3p73S6-Wprq7MLlpBACjxvSE8n9yTP2PK41AfkLnftwnuIGe6rmb25FVNmEyuS3XKaEXPpz0kDqI6t1byJICoHOUt_vqGPlFZyXGCf0MotNcW0mYR8UKXnekjFKTkyWBVId7k5FurCuXkqRYHcXogzzGxY8vTeZ_ECIRF29ucaEnQPiwGEYgs7h9DhRJ88COxHj_kT15mLh8uug0mcTKrE-6OnwrbtRQV-82y5PRURrd4iodFp86lfbuAuke3PdMIYoUSF6EH7ff6NhhpG1bcyVkspkZnZ90FzZiWE5r7a6eD_A
```

## Not so super user:

```bash
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFUUllhVDYtVDhHbnlUMXJYWTFnMSJ9.eyJpc3MiOiJodHRwczovL2FqYWppLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTMzMjFkMzkxOWJjMDA3NmEzOTlhMyIsImF1ZCI6IlBsYXl0aW1lLVRyYWNrZXIiLCJpYXQiOjE2MTEyNjg4MTQsImV4cCI6MTYxMTM1NTIxNCwiYXpwIjoiMEk3NktGSTZ3QUlQRVdrMEYzeHdNNjJiS1NUWVB1c3UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDptb3N0LXBsYXl0aW1lIiwiZ2V0OnBsYXl0aW1lL2lkIiwiZ2V0OnBsYXl0aW1lcyJdfQ.BkLBCmU9cQWrZ6bcfT1M6jUa7dogPJRUMvqp1jq0fKcrWBGoErBBacpTUoohdiazJg4gBKMSd4C38LRJHpaKitnlT5YXDtlvZlTW0jiPAkSRETu5uHUAAZrxE_6gccnbPpBFmzRxnm5AhWOKZsXIN8QVln5j5T5tinTlA1Aks6kdy0lX-c0aU_JMWRy_AgdiAKVPo_MovB4qsHtHQdcAg1mZfFf3xt4yXFc9eh2A7XNmxS3zoQv5zFydnM0fHLNQflsNghN_Dt-cgxYkbXEBPM6eLjUiW6f_2EdnDDx7Xa22paxrs7xeTdGSgt-Z9DaPEXfGpbpE3jvZm1LlNFQ1Ew
```

# APIs

## Playtime APIs

# get_all_playtimes:

GET requests for getting details of all playtimes.

# Method URI

```bash
Get https://ajaji-playtime-tracker.herokuapp.com/playtimes
```

# Response

```bash
{
    "Playtimes": [
        {
            "game": "Overwatch",
            "genre": "Shooter",
            "player_id": 1,
            "playtime": "23:40:00",
            "playtime_id": 1
        }
    ],
    "success": true
}
```

# get_playtime:

GET requests for getting total playtime for all games for id player.

# Method URI

```bash
Get https://ajaji-playtime-tracker.herokuapp.com/playtime/<int:player_id>
```

# Response

```bash
{
    "Your total gaming time is": "23:40:00",
    "success": true
}
```

# get_most_played:

GET requests for getting most played game for all players.

# Method URI

```bash
Get https://ajaji-playtime-tracker.herokuapp.com/most-playtime
```

# Response

```bash
{
    "Most played game": "Overwatch",
    "Time played": "23:40:00",
    "success": true
}
```

# create_playtime:

POST requests for creating new record in Playtime table..

# Method URI

```bash
Post https://ajaji-playtime-tracker.herokuapp.com/playtime
```

# Request

```bash
{
    "game": "Overwatch",
    "player": "Abdullah",
    "playtime": "23:40",
    "genre": "Shooter"
}
```

# Response

```bash
{
    "Game Added": {
        "game": "Overwatch",
        "genre": "Shooter",
        "player_id": 1,
        "playtime": "23:40:00",
        "playtime_id": 1
    },
    "success": true
}
```

# update_playtime:

PATCH requests for updating playtime record.

# Method URI

```bash
Patch https://ajaji-playtime-tracker.herokuapp.com/playtime/<int:p_id>
```

# Request

```bash
{
    "game": "Fifa",
    "playtime": "23:40",
    "genre": "Shooter"
}
```

# Response

```bash
{
    "Playtime updated": {
        "game": "Fifa",
        "genre": "Shooter",
        "player_id": 1,
        "playtime": "23:40:00",
        "playtime_id": 1
    },
    "success": true
}
```

# update_playtime:

DELETE requests for deleting playtime record.

# Method URI

```bash
Delete https://ajaji-playtime-tracker.herokuapp.com/playtime/<int:p_id>
```

# Response

```bash
{
    "Playtime ID": 1,
    "success": true
}
```

## Motivation for project

I always like to keep track of my gaming hours and I thought it would be fun to create and app to help with that.
