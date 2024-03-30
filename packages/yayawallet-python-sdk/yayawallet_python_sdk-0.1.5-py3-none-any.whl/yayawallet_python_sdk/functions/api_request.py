import os
import httpx
from get_time import get_time
from typing import Dict
from generate_signature import generate_signature
import json

async def api_request(
    method: str,
    path: str,
    params: str,
    data: Dict = None,
):    
    url = os.getenv("YAYA_API_URL") + path + params
    YAYA_API_PATH = os.getenv("YAYA_API_PATH") + path

    unix_time_response = await get_time()
    unix_time = unix_time_response.time
    json_body = json.dump(data)
    signed_payload = generate_signature(unix_time, method, YAYA_API_PATH, json_body)
        
    headers = {
        "YAYA-API-KEY": os.getenv("YAYA_API_KEY"),
        "YAYA-API-TIMESTAMP": unix_time,
        "YAYA-API-SIGN": signed_payload,
    }
        
    if(method == "POST"):
        response = httpx.post(url, headers=headers, data=data)
    if(method == "PUT"):
        response = httpx.put(url, headers=headers, data=data)
    response = httpx.get(url, headers=headers)
    return response.text()
