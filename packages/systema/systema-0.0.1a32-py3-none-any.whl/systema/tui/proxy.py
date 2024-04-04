from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any, Generator, Generic, Literal, TypeVar

import httpx

from systema.management import InstanceType, settings
from systema.models.bin import Bin, BinCreate, BinRead, BinUpdate
from systema.models.card import Card, CardCreate, CardRead, CardUpdate
from systema.models.item import (
    Item,
    ItemCreate,
    ItemRead,
    ItemUpdate,
)
from systema.models.project import (
    Project,
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
)

T = TypeVar("T")


class Proxy(ABC, Generic[T]):
    @cached_property
    def client(self):
        if token := settings.token:
            return httpx.Client(
                headers={"Authorization": f"Bearer {token}"}, follow_redirects=True
            )
        raise ValueError("No token")

    @property
    def base_url(self) -> str:
        return str(settings.server_base_url)

    def is_set_as_server(self):
        return settings.instance_type == InstanceType.SERVER

    @abstractmethod
    def all(self) -> Generator[T, None, None]:
        pass

    @abstractmethod
    def create(self, data: Any) -> T:
        pass

    @abstractmethod
    def update(self, id: str, data: Any) -> T:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass


class ProjectProxy(Proxy[ProjectRead]):
    @property
    def base_url(self) -> str:
        return super().base_url + "projects/"

    def all(self):
        if self.is_set_as_server():
            return Project.list()
        response = self.client.get(self.base_url)
        response.raise_for_status()
        return (ProjectRead(**p) for p in response.json())

    def create(self, data: ProjectCreate):
        if self.is_set_as_server():
            return Project.create(data)
        response = self.client.post(self.base_url, json=data.model_dump(mode="json"))
        response.raise_for_status()
        return ProjectRead(**response.json())

    def update(self, id: str, data: ProjectUpdate):
        if self.is_set_as_server():
            return Project.update(id, data)
        response = self.client.patch(
            f"{self.base_url}{id}/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        response.raise_for_status()
        return ProjectRead(**response.json())

    def delete(self, id: str):
        if self.is_set_as_server():
            return Project.delete(id)
        response = self.client.delete(f"{self.base_url}{id}/")
        response.raise_for_status()


class ItemProxy(Proxy[ItemRead]):
    def __init__(self, project_id: str):
        self.project_id = project_id

    @property
    def base_url(self) -> str:
        return super().base_url + f"projects/{self.project_id}/items/"

    def all(self):
        if self.is_set_as_server():
            return Item.list(self.project_id)
        response = self.client.get(self.base_url)
        response.raise_for_status()
        return (ItemRead(**p) for p in response.json())

    def create(self, data: ItemCreate):
        if self.is_set_as_server():
            return Item.create(data, self.project_id)
        response = self.client.post(self.base_url, json=data.model_dump(mode="json"))
        response.raise_for_status()
        return ItemRead(**response.json())

    def update(self, id: str, data: ItemUpdate):
        if self.is_set_as_server():
            return Item.update(self.project_id, id, data)
        response = self.client.patch(
            f"{self.base_url}{id}/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        response.raise_for_status()
        return ItemRead(**response.json())

    def delete(self, id: str):
        if self.is_set_as_server():
            Item.delete(self.project_id, id)
        response = self.client.delete(f"{self.base_url}{id}/")
        response.raise_for_status()

    def move(self, id: str, up_or_down: Literal["up", "down"]):
        if self.is_set_as_server():
            return Item.move(self.project_id, id, up_or_down)
        response = self.client.post(f"{self.base_url}{id}/{up_or_down}")
        response.raise_for_status()
        return ItemRead(**response.json())

    def toggle(self, id: str):
        if self.is_set_as_server():
            return Item.check_or_uncheck(self.project_id, id)
        response = self.client.post(f"{self.base_url}{id}/toggle")
        response.raise_for_status()
        return ItemRead(**response.json())


class BinProxy(Proxy[BinRead]):
    def __init__(self, board_id: str):
        self.board_id = board_id

    @property
    def base_url(self) -> str:
        return super().base_url + f"projects/{self.board_id}/bins/"

    def all(self):
        if self.is_set_as_server():
            return Bin.list(self.board_id)
        response = self.client.get(self.base_url)
        response.raise_for_status()
        return (BinRead(**p) for p in response.json())

    def create(self, data: BinCreate):
        if self.is_set_as_server():
            return Bin.create(data, self.board_id)
        response = self.client.post(self.base_url, json=data.model_dump(mode="json"))
        response.raise_for_status()
        return BinRead(**response.json())

    def update(self, id: str, data: BinUpdate):
        if self.is_set_as_server():
            return Bin.update(self.board_id, id, data)
        response = self.client.patch(
            f"{self.base_url}{id}/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        response.raise_for_status()
        return BinRead(**response.json())

    def delete(self, id: str):
        if self.is_set_as_server():
            Bin.delete(self.board_id, id)
        response = self.client.delete(f"{self.base_url}{id}/")
        response.raise_for_status()

    def move(self, id: str, direction: Literal["left", "right"]):
        if self.is_set_as_server():
            return Bin.move(self.board_id, id, direction)
        response = self.client.post(
            f"{self.base_url}{id}/move/{direction}",
        )
        response.raise_for_status()
        return BinRead(**response.json())


class CardProxy(Proxy[CardRead]):
    def __init__(self, board_id: str):
        self.board_id = board_id

    @property
    def base_url(self) -> str:
        return super().base_url + f"projects/{self.board_id}/cards/"

    def all(self):
        if self.is_set_as_server():
            return Card.list(self.board_id)
        response = self.client.get(self.base_url)
        response.raise_for_status()
        return (CardRead(**r) for r in response.json())

    def create(self, data: CardCreate):
        if self.is_set_as_server():
            return Card.create(data, self.board_id)
        response = self.client.post(self.base_url, json=data.model_dump(mode="json"))
        response.raise_for_status()
        return CardRead(**response.json())

    def update(self, id: str, data: CardUpdate):
        if self.is_set_as_server():
            return Card.update(self.board_id, id, data)
        response = self.client.patch(
            f"{self.base_url}{id}/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        response.raise_for_status()
        return CardRead(**response.json())

    def delete(self, id: str):
        if self.is_set_as_server():
            Card.delete(self.board_id, id)
        response = self.client.delete(f"{self.base_url}{id}/")
        response.raise_for_status()

    def move(self, id: str, direction: Literal["up", "down", "left", "right"]):
        if self.is_set_as_server():
            return Card.move(self.board_id, id, direction)
        response = self.client.post(f"{self.base_url}{id}/move/{direction}")
        response.raise_for_status()
        return CardRead(**response.json())
