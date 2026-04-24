from fastapi import FastAPI, HTTPException

from ..config import get_logger
from ..crud import Crud
from ..schema import UserBase, UserFilter, UserFull

log = get_logger()


def define_routes(app: FastAPI, crud: Crud) -> None:

    @app.post(path="/user/")
    async def post_user(  # pyright: ignore[reportUnusedFunction]
        user: UserBase,
    ) -> UserFull:
        return crud.create_user(user)

    @app.get(path="/user/")
    async def get_user(  # pyright: ignore[reportUnusedFunction]
        filter: str | None = None,
    ):
        return crud.get_users(UserFilter(name=filter))

    @app.get(path="/user/{id}")
    async def get_user_by_id(  # pyright: ignore[reportUnusedFunction]
        id: int,
    ):
        filter = UserFilter(id=id)
        result = crud.get_users(filter)
        if len(result) != 1:
            raise HTTPException(status_code=404, detail=f"No User with id {id}")
        return result[0]

    @app.put(path="/user/")
    async def _put_user(user: UserFull):  # pyright: ignore[reportUnusedFunction]
        try:
            crud.change_user(user)
        except AttributeError as error:
            raise HTTPException(status_code=404, detail=str(error))

    @app.delete(path="/user/{id}/")
    async def _delete_user(id: int):  # pyright: ignore[reportUnusedFunction]
        try:
            return crud.delete_user(id)
        except AttributeError as error:
            log.error(error)
            return HTTPException(status_code=404, detail=f"No User with id {id}")
