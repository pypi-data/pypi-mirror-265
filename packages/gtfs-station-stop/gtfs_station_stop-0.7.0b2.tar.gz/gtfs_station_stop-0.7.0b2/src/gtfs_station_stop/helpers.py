import csv
import os
import time
from collections.abc import Iterable
from datetime import datetime as dt
from io import BytesIO, StringIO
from urllib.parse import urlparse
from zipfile import ZipFile

import requests_cache
from aiohttp_client_cache import CachedSession, SQLiteBackend
from google.transit import gtfs_realtime_pb2

from gtfs_station_stop.const import GTFS_STATIC_CACHE, GTFS_STATIC_CACHE_EXPIRY


def is_none_or_ends_at(
    alert: gtfs_realtime_pb2.FeedEntity, at_time: float | dt | None = None
):
    """Returns the 'ends at' time, else returns None if not active."""
    if at_time is None:
        at_time = time.time()
        # fallthrough
    if isinstance(at_time, float):
        at_time = dt.fromtimestamp(at_time)

    for time_range in alert.active_period:
        start: dt = (
            dt.fromtimestamp(time_range.start)
            if time_range.HasField("start")
            else dt.min
        )
        end: dt = (
            dt.fromtimestamp(time_range.end) if time_range.HasField("end") else dt.max
        )
        if start <= at_time <= end:
            return end

    return None


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except (ValueError, AttributeError):
        return False


def gtfs_record_iter(zip_filelike, target_txt: os.PathLike):
    """Generates a line from a given GTFS table. Can handle local files or URLs."""

    zip_data = zip_filelike
    # If the data is a url, make the request for the file resource.
    if is_url(zip_filelike):
        # Make the request, check for good return code, and convert to IO object.
        # As GTFS Static Data updates rarely, (most providers recommend pulling this once per day),
        # we will use a cache to minimize unnecessary checks.
        session = requests_cache.CachedSession(
            GTFS_STATIC_CACHE, expire_after=GTFS_STATIC_CACHE_EXPIRY
        )
        res = session.get(zip_filelike)
        if 200 <= res.status_code < 400:
            zip_data = BytesIO(res.content)

    with ZipFile(zip_data, "r") as zip:
        # Find the stops.txt file
        first_or_none: str = next(
            (name for name in zip.namelist() if name == target_txt), None
        )
        if first_or_none is None:
            raise RuntimeError(f"Did not find required {target_txt} file")
        # Create the dictionary of IDs, parents should precede the children
        with StringIO(str(zip.read(first_or_none), encoding="ASCII")) as stops_dot_txt:
            reader = csv.DictReader(
                stops_dot_txt,
                delimiter=",",
            )
            for line in reader:
                yield line


async def async_get_gtfs_database(
    gtfs_class, gtfs_urls: Iterable[os.PathLike] | os.PathLike
):
    gtfs_db = gtfs_class()
    if isinstance(gtfs_urls, os.PathLike):
        gtfs_urls = [gtfs_urls]
    for url in gtfs_urls:
        async with CachedSession(
            cache=SQLiteBackend(
                GTFS_STATIC_CACHE, expire_after=GTFS_STATIC_CACHE_EXPIRY
            )
        ) as session:
            async with session.get(url) as response:
                zip_data = BytesIO(await response.read())
                gtfs_db.add_gtfs_data(zip_data)
    return gtfs_db
