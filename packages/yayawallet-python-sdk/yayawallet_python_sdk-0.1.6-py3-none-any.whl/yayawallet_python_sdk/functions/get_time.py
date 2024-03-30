import os
import httpx

async def get_time():
    url = os.getenv("YAYA_API_URL") + '/time'
    response = await httpx.get(url)
    return response.text()