import grpc
from concurrent import futures
from sqlalchemy.orm import Session
from api.config.db import SessionLocal, UserDB
from api.grpc.proto import user_pb2, user_pb2_grpc
from api.config.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from grpc_reflection.v1alpha import reflection

class UserService(user_pb2_grpc.UserServiceServicer):
  
    def HealthCheck(self, request, context):
        try:
            db: Session = SessionLocal()
            is_active_db = db.is_active
            if is_active_db:
                return user_pb2.HealthResponse(health="OK", status=f'{grpc.StatusCode.OK}')
        except Exception as ex:
            print(ex)
            return user_pb2.HealthResponse(health="FAILING", status=f'{grpc.StatusCode.INTERNAL}')
                
    def CreateUser(self, request, context):
        db: Session = SessionLocal()
        existig_user = db.query(UserDB).filter(UserDB.email == request.email).all()
        if len(existig_user):
            return user_pb2.User(id=existig_user[0].id, name=existig_user[0].name, email=existig_user[0].email)
        hashed_password = get_password_hash(request.password)
        db_user = UserDB(name=request.name, email=request.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()
        return user_pb2.User(id=db_user.id, name=db_user.name, email=db_user.email)

    def GetUser(self, request, context):
        db: Session = SessionLocal()
        user = db.query(UserDB).filter(UserDB.id == request.id).first()
        db.close()
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        return user_pb2.User(id=user.id, name=user.name, email=user.email)

    def Authenticate(self, request, context):
        db: Session = SessionLocal()
        user = db.query(UserDB).filter(UserDB.email == request.email).first()
        db.close()
        if not user or not verify_password(request.password, user.hashed_password):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials")

        access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
        return user_pb2.AuthResponse(access_token=access_token, token_type="bearer")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    SERVICE_NAMES = (
        user_pb2.DESCRIPTOR.services_by_name['UserService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
