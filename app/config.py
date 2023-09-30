
# As the project os growing our environment variable is growing that we will gonna use in the project therefore 
# it will be a problem to create it manuallly therfore we need to do it we will create a environment file 
# validoate all te environemnt are righlt set for the production 

from pydantic_settings import BaseSettings


# this is the class we atr making for the environmant variable just like a model 
class Settings(BaseSettings):
    DATABASE_HOSTNAME :str
    DATABASE_PORT : str
    DATABASE_PASSWORD : str 
    DATABASE_NAME : str 
    DATABASE_USERNAME : str 
    SECRET_KEY : str 
    ALGORITHM : str 
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    class Config : 
        env_file = ".env"

settings = Settings()