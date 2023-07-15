from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str


class ProtectedResponse(BaseModel):
    username: str


class UserAuthRequest(BaseModel):
    email: str = Field(..., description='User email')
    password: str = Field(..., max_length=255, description='User password')
