from __future__ import annotations

import json
import pathlib
import typing
import weakref

import requests

from servir._provide import Provider
from servir._tilesets import TilesetResource


def test_files(tmp_path: pathlib.Path) -> None:
    provider = Provider()

    with open(tmp_path / "hello.txt", "w") as f:
        f.write("hello, world")

    server_resource = provider.create(tmp_path / "hello.txt")
    response = requests.get(server_resource.url)
    assert response.text == "hello, world"
    assert "text/plain" in response.headers["Content-Type"]

    response = requests.get(provider.url + "/foo.txt")
    assert response.status_code == 404


def test_file_content_type_json(tmp_path: pathlib.Path) -> None:
    provider = Provider()

    data = {"hello": "world"}

    with open(tmp_path / "hello.json", "w") as f:
        json.dump(data, f)

    server_resource = provider.create(tmp_path / "hello.json")
    response = requests.get(server_resource.url)
    assert response.json() == data
    assert "application/json" in response.headers["Content-Type"]


def test_file_content_type_csv(tmp_path: pathlib.Path) -> None:
    provider = Provider()

    path = tmp_path / "data.csv"

    with open(path, mode="w", newline="\n") as f:
        f.write("a,b,c\n1,2,3\n4,5,6")

    server_resource = provider.create(path)
    response = requests.get(server_resource.url)
    assert response.text == path.read_text()
    assert "text/csv" in response.headers["Content-Type"]


def test_content() -> None:
    provider = Provider()

    content = "hello, world"
    str_resource = provider.create(content)
    response = requests.get(str_resource.url)
    assert response.text == content
    assert "text/plain" in response.headers["Content-Type"]


def test_content_explicit_extension() -> None:
    provider = Provider()
    data = "a,b,c,\n1,2,3,\n4,5,6"

    content_resource = provider.create(data, extension=".csv")
    response = requests.get(content_resource.url)
    assert response.text == data
    assert "text/csv" in response.headers["Content-Type"]


def test_directory_resource(tmp_path: pathlib.Path) -> None:
    provider = Provider()

    root = tmp_path / "data_dir"
    root.mkdir()
    (root / "hello.txt").write_text("hello, world")
    (root / "nested_dir").mkdir()
    (root / "nested_dir" / "foo.txt").write_text("foo")

    server_resource = provider.create(root)
    print(server_resource.url)

    response = requests.get(server_resource.url + "/hello.txt")
    assert response.text == "hello, world"

    response = requests.get(server_resource.url + "/nested_dir/foo.txt")
    assert response.text == "foo"


def test_tileset_resource() -> None:
    provider = Provider()

    class Tileset:
        @property
        def uid(self) -> str:
            return "aaaaaaaaaa"

        def tiles(self, tile_ids: typing.Sequence[str]) -> list[typing.Any]:
            return [(tid, None) for tid in tile_ids]

        def info(self) -> typing.Any:
            return "tile_info"

    tileset = Tileset()
    resource = provider.create(tileset)
    assert isinstance(resource, TilesetResource)

    resource_url = f"{resource.server}tileset_info/?d={resource.uid}"
    info = requests.get(resource_url).json()
    assert info[resource.uid] == "tile_info"
    tile_url = resource_url.replace("tileset_info", "tiles") + ".0.0"
    tiles = requests.get(tile_url).json()
    assert f"{resource.uid}.0.0" in tiles


def test_resource_cleanup() -> None:
    provider = Provider()
    assert not provider._resources

    content = "hello, world"

    resource1 = provider.create(content)
    resource_ref = weakref.ref(resource1)
    assert len(provider._resources) == 1

    resource2 = provider.create(content)
    assert resource1 == resource2
    assert len(provider._resources) == 1

    # should not trigger cleanup
    del resource1
    assert len(provider._resources) == 1
    assert resource_ref() is resource2

    # should trigger cleanup
    del resource2
    assert len(provider._resources) == 0
    assert resource_ref() is None
