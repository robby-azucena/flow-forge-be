from starlette.datastructures import Headers


async def get_client_ip(headers: Headers, path:str) -> str:
    x_forwarded_for = headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return headers.get("X-Forwarded-For", "")