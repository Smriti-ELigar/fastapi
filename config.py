# this file holds all the environment settings for the application. it is used to configure the database connection, the secret key for JWT authentication, and other settings. it is a good practice to keep all the configuration settings in a separate file so that they can be easily changed without modifying the code. this file is imported in the main.py file and the settings are used to configure the application.
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_url: str
    log_file: str = "app.log"
    origins: List[str] =["*"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  

settings = Settings()