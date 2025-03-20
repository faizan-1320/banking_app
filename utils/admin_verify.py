from functools import wraps
from fastapi import Depends,HTTPException,status
from models import User
from tokenUser import verify_token

def admin_required(func):
    @wraps(func)
    def wrapper(*args, current_user: User = Depends(verify_token), **kwargs):

        # Check if the user is an admin
        if current_user.userType.value != "Admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action."
            )

        # Call the original function
        return func(*args, **kwargs)

    return wrapper
