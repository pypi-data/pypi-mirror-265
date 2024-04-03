from typing import Tuple

import pandas as pd

from ..logging import logger
from ..utils import change_crs, change_timezone, get_crs, get_timezone

DEFAULT_CRS_SENSOR = "EPSG:4326"


def set_timezone(
    df: pd.DataFrame,
    timezone: str | None | Tuple[str, str] = None,
) -> Tuple[pd.DataFrame, str]:
    if isinstance(timezone, tuple) and len(timezone) == 2:
        source_tz = timezone[0]
        target_tz = timezone[1]
        df = change_timezone(df, source_tz, target_tz)
        timezone = target_tz
    elif not timezone:
        timezone = get_timezone(df)

    return df, timezone


def set_crs(
    df: pd.DataFrame,
    crs: str | None | Tuple[str, str] = None,
) -> Tuple[pd.DataFrame, str]:
    if isinstance(crs, tuple) and len(crs) == 2:
        source_crs = crs[0]
        target_crs = crs[1]
        df = change_crs(df, source_crs, target_crs)
        crs = target_crs
    elif isinstance(crs, str):
        df = change_crs(df, DEFAULT_CRS_SENSOR, crs)
    elif not crs:
        crs = get_crs(df)
        df = change_crs(df, DEFAULT_CRS_SENSOR, crs)
    else:
        logger.error(f"Invalid value for crs: {crs}")

    return df, crs
