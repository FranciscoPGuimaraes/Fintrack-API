import re
from fastapi import HTTPException
from psycopg2 import IntegrityError
from fintrack_api.services.db import connect
from fintrack_api.models.userModels import UserIn


async def create_user(user: UserIn) -> None:
    query = """INSERT INTO "user"(name, email, password) 
               VALUES (%(name)s, %(email)s, %(password)s);"""
    parameters = {
        'name': user.name,
        'email': user.email,
        'password': user.password,
    }
    try:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, parameters)
            conn.commit()
    except IntegrityError as e:
        error = re.search(r'Key \((.*?)\)=\((.*?)\) already exists', e.pgerror)
        raise HTTPException(
            status_code=400, 
            detail=f"User with {error.group(1)} {error.group(2)} already exists."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
