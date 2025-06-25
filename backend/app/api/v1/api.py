from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, children, playdates, interests, user_lists

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(children.router, prefix="/children", tags=["children"])
api_router.include_router(playdates.router, prefix="/playdates", tags=["playdates"])
api_router.include_router(interests.router, prefix="/interests", tags=["interests"])
api_router.include_router(user_lists.router, prefix="/user-lists", tags=["user-lists"])