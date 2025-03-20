from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Account,UserAccount,User
from schemas import NewAccount,UpdateAccount,ViewUserAccount,ViewUser,ViewAccount
from tokenUser import verify_token
from utils.admin_verify import admin_required

router = APIRouter(tags=['admin'])

@router.post('/create-account',status_code=status.HTTP_201_CREATED)
@admin_required
def create_account(request: NewAccount, db: Session = Depends(get_db),current_user: User = Depends(verify_token)):
    account = db.query(Account).filter(Account.accountNumber==request.accountNumber).first()
    if account:
        raise HTTPException(detail={'error':'Account already exists'},status_code=status.HTTP_400_BAD_REQUEST)
    new_account = Account(
        branchName=request.branchName,
        accountNumber=request.accountNumber,
        ifscCode=request.ifscCode,
        bankAddress=request.bankAddress,
        accountType=request.accountType
    )
    db.add(new_account)
    db.flush()

    user_account_add = UserAccount(
        accountId=new_account.id,
        userId=request.userId
    )
    db.add(user_account_add)
    
    db.commit()
    db.refresh(new_account)
    
    return JSONResponse(content={'message': 'Account created successfully!'})

@router.patch('/update-account/{user_id}')
@admin_required
def update_accout(user_id:int,request:UpdateAccount,db:Session=Depends(get_db),current_user: User = Depends(verify_token)):
    user_account = db.query(UserAccount).filter(UserAccount.userId==user_id).first()

    if not user_account:
        raise HTTPException(detail={'error':'User Not Found'},status_code=status.HTTP_404_NOT_FOUND)
    
    update_account =db.query(Account).filter(Account.id==user_account.accountId).first()

    if not update_account:
        raise HTTPException(detail={'error': 'Account Not Found'}, status_code=status.HTTP_404_NOT_FOUND)
    
    if request.accountType:
        update_account.accountType = request.accountType
    if request.branchName:
        update_account.branchName = request.branchName
    if request.accountNumber:
        update_account.accountNumber = request.accountNumber
    if request.bankAddress:
        update_account.bankAddress = request.bankAddress
    if request.ifscCode:
        update_account.ifscCode = request.ifscCode

    db.commit()
    db.refresh(update_account)

    return {
        "message": "Account updated successfully",
        "updated_account": {
            "accountId": update_account.id,
            "accountType": update_account.accountType,
            "branchName": update_account.branchName,
            "accountNumber": update_account.accountNumber,
            "bankAddress": update_account.bankAddress,
            "ifscCode": update_account.ifscCode
        }
    }

@router.delete('/delete-account/{user_id}')
@admin_required
def delete_account(user_id:int,db:Session=Depends(get_db),current_user: User = Depends(verify_token)):
    user_account = db.query(UserAccount).filter(UserAccount.userId==user_id).first()

    if not user_account:
        raise HTTPException(detail={'error':'User Not Found'},status_code=status.HTTP_404_NOT_FOUND)
    
    update_account =db.query(Account).filter(Account.id==user_account.accountId).first()

    if not update_account:
        raise HTTPException(detail={'error': 'Account Not Found'}, status_code=status.HTTP_404_NOT_FOUND)
    
    db.delete(user_account)
    db.delete(update_account)
    db.commit()
    return {'message':'Account deleted successfully'}

@router.get('/all-accounts', response_model=list[ViewUserAccount])
@admin_required
def get_all_user_accounts(db: Session = Depends(get_db),current_user: User = Depends(verify_token)):
    user_accounts = db.query(UserAccount).all()

    if not user_accounts:
        raise HTTPException(status_code=404, detail="No user accounts found")

    user_dict = {}

    for user_account in user_accounts:
        user = user_account.user
        account = user_account.account

        if user and account:
            user_id = user.id

            if user_id not in user_dict:
                user_dict[user_id] = {
                    "user": ViewUser.model_validate(user),
                    "accountDetail": []
                }
            user_dict[user_id]["accountDetail"].append(ViewAccount.model_validate(account))

    result = list(user_dict.values())

    return result
