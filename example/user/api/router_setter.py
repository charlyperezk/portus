from fastapi import APIRouter
from example.user.dtos import UserCreateDTO, UserReadDTO, UserUpdateDTO
from example.user.service import UserService
from src.portus.adapters.input.rest_controller import set_controller

def set_user_routes(router: APIRouter):
    return set_controller(
        router,
        UserService(),
        UserCreateDTO,
        UserReadDTO, 
        UserUpdateDTO
    )