import ipaddress

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from starlette.status import HTTP_403_FORBIDDEN

from config.settings import settings
from constants.response_message import IP_NOT_ALLOWED


def setup_ip_whitelist(app:FastAPI) -> None:

    networks = [
        ipaddress.ip_network(ip.strip(), strict=False)
        for ip in settings.ALLOWED_IPS.split(",")
        if ip.strip()
    ]

    @app.middleware("http")
    async def ip_whitelist(request: Request, call_next):
        try:
            client_ip = ipaddress.ip_address(request.client.host)
        except (ValueError, AttributeError):
            return JSONResponse(IP_NOT_ALLOWED, status_code=HTTP_403_FORBIDDEN)

        if not any(client_ip in net for net in networks):
            return JSONResponse(IP_NOT_ALLOWED, status_code=HTTP_403_FORBIDDEN)

        return await call_next(request)
