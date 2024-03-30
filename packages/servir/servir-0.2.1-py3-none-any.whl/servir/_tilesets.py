from __future__ import annotations

import itertools
import typing

from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import Mount, Route
from starlette.types import ASGIApp, Receive, Scope, Send

from servir._protocols import ProviderProtocol, TilesetProtocol

# HiGlass


_MOUNT_PATH = "/tilesets/api/v1/"

TilesetType = typing.TypeVar("TilesetType", bound=TilesetProtocol)


class TilesetResource(typing.Generic[TilesetType]):
    """A tileset resource."""

    def __init__(self, tileset: TilesetType, provider: ProviderProtocol):
        """Initialize a tileset resource.

        Parameters
        ----------
        tileset : TilesetProtocol
            The tileset.
        provider : ProviderProtocol
            The server provider.
        """
        self._tileset = tileset
        self._provider = provider

    @property
    def tileset(self) -> TilesetType:
        """The tileset."""
        return self._tileset

    @property
    def uid(self) -> str:
        """The unique identifier for the tileset."""
        return self._tileset.uid

    @property
    def server(self) -> str:
        """The server url."""
        return f"{self._provider.url}{_MOUNT_PATH}"


def get_list(query: str, field: str) -> list[str]:
    """Parse chained query params into list.

    Parameters
    ----------
    query : str
        The query string. For example, "d=id1&d=id2&d=id3".
    field : str
        The field to extract. For example, "d".

    Returns
    -------
    list[str]
        The list of values for the given field. For example, ['id1', 'id2', 'id3'].
    """
    kv_tuples = [x.split("=") for x in query.split("&")]
    return [v for k, v in kv_tuples if k == field]


def tileset_info(
    request: Request, tilesets: typing.Mapping[str, TilesetResource[TilesetProtocol]]
) -> JSONResponse:
    """Request handler for the tileset_info/ endpoint.

    Parameters
    ----------
    request : Request
        The request.
    tilesets : typing.Mapping[str, TilesetResource]
        The tileset resources.

    Returns
    -------
    JSONResponse
        The server response.
    """
    uids = get_list(request.url.query, "d")
    info = {
        uid: tilesets[uid].tileset.info()
        if uid in tilesets
        else {"error": f"No such tileset with uid: {uid}"}
        for uid in uids
    }
    return JSONResponse(info)


def tiles(
    request: Request, tilesets: typing.Mapping[str, TilesetResource[TilesetProtocol]]
) -> JSONResponse:
    """Request handler for the tiles/ endpoint.

    Parameters
    ----------
    request : Request
        The request.
    tilesets : typing.Mapping[str, TilesetResource]
        The tileset resources.

    Returns
    -------
    JSONResponse
        The server response.
    """
    requested_tids = set(get_list(request.url.query, "d"))
    if not requested_tids:
        return JSONResponse({"error": "No tiles requested"}, 400)

    tiles: list[typing.Any] = []
    for uid, tids in itertools.groupby(
        iterable=sorted(requested_tids), key=lambda tid: tid.split(".")[0]
    ):
        tileset_resource = tilesets.get(uid)
        if not tileset_resource:
            return JSONResponse(
                {"error": f"No tileset found for requested uid: {uid}"}, 400
            )
        tiles.extend(tileset_resource.tileset.tiles(list(tids)))
    data = {tid: tval for tid, tval in tiles}
    return JSONResponse(data)


def chromsizes(
    request: Request, tilesets: typing.Mapping[str, TilesetResource[TilesetProtocol]]
) -> PlainTextResponse | JSONResponse:
    """Request handler for the chrom-sizes/ endpoint.

    Chromsizes are returned as a plain text response, as a TSV:

        chr1    249250621
        chr2    243199373
        ...

    Parameters
    ----------
    request : Request
        The request.
    tilesets : typing.Mapping[str, TilesetResource]
        The tileset resources.

    Returns
    -------
    PlainTextResponse | JSONResponse
        The server response. If the tileset does not have chromsizes, a JSON
        response with an error message is returned.
    """
    uid = request.query_params.get("id")
    if uid is None:
        return JSONResponse({"error": "No uid provided."}, 400)
    tileset_resource = tilesets[uid]
    info = tileset_resource.tileset.info()
    assert "chromsizes" in info, "No chromsizes in tileset info"
    return PlainTextResponse(
        "\n".join(f"{chrom}\t{size}" for chrom, size in info["chromsizes"])
    )


TilesetEndpoint = typing.Callable[
    [Request, typing.Mapping[str, TilesetResource[TilesetProtocol]]], Response
]


def create_tileset_route(
    tileset_resources: typing.Mapping[str, TilesetResource[TilesetProtocol]],
    scope_id: str = "tilesets",
) -> Mount:
    """Create a route for tileset endpoints.

    Parameters
    ----------
    tileset_resources : typing.Mapping[str, TilesetResource]
        The tileset resources.
    scope_id : str, optional
        The scope id to use for passing the tileset resources to the
        request handlers, by default "tilesets".

    Returns
    -------
    Mount
        The API route.
    """

    class TilesetMiddleware:
        """Middleware to inject tileset resources into request scope."""

        def __init__(self, app: ASGIApp) -> None:
            self.app = app

        async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
            scope[scope_id] = tileset_resources
            await self.app(scope, receive, send)

    def inject_tilesets(func: TilesetEndpoint) -> typing.Callable[[Request], Response]:
        """Inject tileset resources as secondrequest handler."""

        def wrapper(request: Request) -> Response:
            return func(request, request.scope[scope_id])

        return wrapper

    return Mount(
        path=_MOUNT_PATH,
        routes=[
            Route("/tileset_info/", inject_tilesets(tileset_info)),
            Route("/tiles/", inject_tilesets(tiles)),
            Route("/chrom-sizes/", inject_tilesets(chromsizes)),
        ],
        middleware=[Middleware(TilesetMiddleware)],
    )
