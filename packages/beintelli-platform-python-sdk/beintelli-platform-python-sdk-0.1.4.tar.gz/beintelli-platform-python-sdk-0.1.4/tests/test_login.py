"""Containing the tests for the log in"""
import pytest
from tests.credentials import Credential
from src.beintelli_platform_python_sdk_eliasinguanta.user import User

@pytest.mark.asyncio
async def test_login():
    """tests login with correct credentials"""
    student: User = User()
    try:
        await (await student.login(Credential.USERNAME.value,Credential.PASSWORD.value))
    except Exception as e:
        print(str(e))
        assert False
