# Social Media API - Follows and Feed

## Follows
- **Follow a user:**
  - `POST /api/accounts/follow/<user_id>/`
  - Requires authentication (Token in `Authorization` header)
- **Unfollow a user:**
  - `POST /api/accounts/unfollow/<user_id>/`
  - Requires authentication

## Feed
- **Get feed:**
  - `GET /api/feed/`
  - Returns posts from users you follow, ordered by creation date (most recent first)
  - Requires authentication

### Example Usage (with curl):

```
curl -X POST http://127.0.0.1:8000/api/accounts/follow/2/ -H "Authorization: Token <your_token>"
curl -X POST http://127.0.0.1:8000/api/accounts/unfollow/2/ -H "Authorization: Token <your_token>"
curl -X GET http://127.0.0.1:8000/api/feed/ -H "Authorization: Token <your_token>"
```

- Replace `<your_token>` with your actual token.
- Replace `2` with the user ID you want to follow/unfollow.

## Notes
- You cannot follow or unfollow yourself.
- The feed only shows posts from users you follow.
