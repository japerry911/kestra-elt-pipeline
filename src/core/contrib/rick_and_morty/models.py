from pydantic import BaseModel


class CharacterLocation(BaseModel):
    name: str
    url: str


class Character(BaseModel):
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    origin: CharacterLocation
    location: CharacterLocation
    image: str
    episode: list[str]
    url: str
    created: str


class Location(BaseModel):
    id: int
    name: str
    type: str
    dimension: str
    residents: list[str]
    url: str
    created: str


class Episode(BaseModel):
    id: int
    name: str
    air_date: str
    episode: str
    characters: list[str]
    url: str
    created: str
