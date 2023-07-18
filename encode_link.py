from hashlib import sha512

from fastapi import FastAPI

app = FastAPI()


@app.get('/encode_link/')
async def encode_link(link: str) -> dict[str, str]:
    """Encodes link to sha512."""
    encoded_link = sha512(link.encode('utf-8')).hexdigest()
    return {'encoded_link': encoded_link}
