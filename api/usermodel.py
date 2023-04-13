from pydantic import BaseModel
from pydantic import Field

class UsersData(BaseModel):
    
    Region: str = Field(default="northeast")
    Gender: str = Field(default="male")
    Smoker: str = Field(default="yes")
    Children: int = Field(default=4)
    Age: int = Field(default=89)
    Bmi: int = Field(default=20)
