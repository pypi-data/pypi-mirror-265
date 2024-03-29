from ..functions.api_request import api_request

async def get_organization():
  api_response = await api_request("GET", "/user/organization", "", None)
  return api_response

async def get_profile(account_name: str):
  api_response = await api_request("POST", "/user/profile",'', {"account_name": account_name})
  return api_response