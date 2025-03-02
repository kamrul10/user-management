from sdk import rest_client

print("Rest api health check")
print(rest_client.health_check())

print("Creating user via REST...")
print(rest_client.create_user("John Doe", "john@example.com", "test_password"))

print("Login user via REST...")
print(rest_client.login("john@example.com", "test_password"))

