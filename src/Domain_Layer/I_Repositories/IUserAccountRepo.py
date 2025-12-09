from abc import ABC
from src.Domain_Layer.I_Repositories.IBaseRepo import IBaseRepo
from src.Domain_Layer.Entities.UserAccount import UserAccount     

class IUserAccountRepo(IBaseRepo[UserAccount], ABC):
    pass
