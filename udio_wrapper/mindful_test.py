import UdioWrapper


auth_token = "%5B%22eyJhbGciOiJIUzI1NiIsImtpZCI6IlJHVktoVzNNcSsyVzhxcDkiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzE0MjEzNjIyLCJpYXQiOjE3MTQyMTAwMjIsImlzcyI6Imh0dHBzOi8vbWZtcHhqZW1hY3NoZmNwem9zbHUuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6IjgwM2Q4MTNjLWZiMDgtNDcyYy1hMGJjLTk1OGZiNzIxNGQ5MSIsImVtYWlsIjoic29mdHdhcmUuYXJ0ZXNhbnM0MkBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6Imdvb2dsZSIsInByb3ZpZGVycyI6WyJnb29nbGUiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0lrVnM3Y2hYNVFOWGtNQk5mUlBlWlc5ZFJ2M0VQZUEteGx6ZVNkZXc5QXh5Z3paQT1zOTYtYyIsImVtYWlsIjoic29mdHdhcmUuYXJ0ZXNhbnM0MkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoiQ3JhZnQgTWFucyIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiJDcmFmdCBNYW5zIiwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSWtWczdjaFg1UU5Ya01CTmZSUGVaVzlkUnYzRVBlQS14bHplU2RldzlBeHlnelpBPXM5Ni1jIiwicHJvdmlkZXJfaWQiOiIxMDQ4MDgwOTg2ODI1NzE1ODQ3NzYiLCJzdWIiOiIxMDQ4MDgwOTg2ODI1NzE1ODQ3NzYifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJvYXV0aCIsInRpbWVzdGFtcCI6MTcxNDIxMDAyMn1dLCJzZXNzaW9uX2lkIjoiYTJiZDVjMjctYmZhOC00YWFlLWIzNGYtMzZiODRlMjBkNmEyIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.VfQiwzpLEVyNDDyEL2_VK3pmXvNvhaTclB5el4SJQhc%22%2C%2273N9fQjcn_oUXwu6v2EaTg%22%2C%22ya29.a0Ad52N38sFcZad6imLgB5tZ2y9ytXqw6hLL3FsVw8LIggcUNEW7nJVez-qLQVYMYzYjcDezUgc_AS8U5maqwr9ekvgWHI1PkRnuqSQcXS8uGvMt2M47kLGOzoClyGtjG3CLZE5JUoZzGfQkQ_FGMZLiF4ZE-w8urNI1fdaCgYKAbYSARMSFQHGX2MilNwkeRnvrotUwwdvcNT7xg0171%22%2Cnull%2Cnull%5D"  # Replace this with your actual authentication token
udio_wrapper = UdioWrapper(auth_token)


short_song_no_download = udio_wrapper.create_song(
    prompt="Relaxing jazz and soulful music",
    seed=-1,
    custom_lyrics="Short song lyrics here"
)


print("Short song generated without downloading:", short_song_no_download)