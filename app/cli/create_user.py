import asyncio
import argparse

from app.core.database import AsyncSessionLocal
from app.crud.user import create_user, get_user_by_username


async def create_user_cli(username: str, password: str):
    async with AsyncSessionLocal() as db:
        exists = await get_user_by_username(db, username)
        if exists:
            print(f"User {username} already exists.")
            return

        await create_user(db, username, password)
        print(f"User created: {username}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()

    asyncio.run(create_user_cli(args.username, args.password))


if __name__ == "__main__":
    main()
