import json

from pydantic import BaseModel, Field


class Config(BaseModel):
    log_level: str
    log_dir: str
    gateway_ip: str
    refresh_interval: int = Field(gt=0)
    bind_address: str
    allow_dht: bool
    rtorrent_xmlrpc_url: str


with open("conf/app.json", "r", encoding="utf-8") as file:
    data = json.load(file)
settings: Config = Config.model_validate(data)
