from sdk import grpc_client

# Health check
print("Health check via gRPC...")
health = grpc_client.health_check()
print(health)

# Create a user
print("Creating user via gRPC...")
user = grpc_client.create_user("Jane Doe", "jane@example.com", "securepassword")
print(user)

# Get user by ID
print("Fetching user via gRPC...")
retrieved_user = grpc_client.get_user(user.id)
print(retrieved_user)

# Authenticate user
print("Authenticating via gRPC...")
auth_response = grpc_client.authenticate("jane@example.com", "securepassword")
print(auth_response)