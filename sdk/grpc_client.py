import grpc

from api.grpc.proto import user_pb2, user_pb2_grpc

host = 'localhost:50051'
def health_check():
    channel = grpc.insecure_channel(host)
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = user_pb2.HealthCheckRequest()
    return stub.HealthCheck(request)

def create_user(name, email, password):
    channel = grpc.insecure_channel(host)
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = user_pb2.CreateUserRequest(name=name, email=email, password=password)
    return stub.CreateUser(request)

def get_user(user_id):
    channel = grpc.insecure_channel(host)
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = user_pb2.GetUserRequest(id=user_id)
    return stub.GetUser(request)

def authenticate(email, password):
    channel = grpc.insecure_channel(host)
    stub = user_pb2_grpc.UserServiceStub(channel)
    request = user_pb2.AuthRequest(email=email, password=password)
    return stub.Authenticate(request)