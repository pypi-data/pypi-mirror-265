from typing import Any, Dict, Tuple

import geopandas as gpd
import pandas as pd
import pydeck as pdk
from shapely.geometry import Point

from ..utils import convert_to_geodataframe


def timeline_layer(df: pd.DataFrame, crs: str | None = None) -> Tuple[pdk.Layer, Point]:
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=crs)  # type: ignore
    center = gdf.geometry.centroid.to_crs(epsg=4326).unary_union.centroid

    gdf["duration"] = gdf["duration"].dt.total_seconds()
    gdf["start"] = gdf["start"].dt.strftime("%Y-%m-%d %H:%M:%S")
    gdf["end"] = gdf["end"].dt.strftime("%Y-%m-%d %H:%M:%S")

    gdf.to_crs(epsg=4326, inplace=True)
    gdf = gdf.astype(
        {
            "trip_id": "float64",
            "stationary_id": "float64",
            "status": "object",
            "mode": "object",
        }
    )  # type: ignore

    geojson = gdf.__geo_interface__  # type: ignore

    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson,
        stroked=False,
        filled=True,
        get_position="geometry.coordinates",
        get_radius=10,  # Radius is in meters
        get_fill_color=[255, 0, 0],
        get_line_color=[127, 0, 0],
        get_line_width=5,
        pickable=True,
        auto_highlight=True,
    )

    return layer, center


def gps_layer(
    df: pd.DataFrame,
    crs: str | None = None,
) -> Tuple[pdk.Layer, Point]:
    gdf = convert_to_geodataframe(df, crs=crs)
    gdf.to_crs(epsg=4326, inplace=True)
    center = gdf.geometry.unary_union.centroid
    geojson = gdf.__geo_interface__  # type: ignore
    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson,
        stroked=False,
        filled=True,
        get_position="geometry.coordinates",
        get_radius=10,  # Radius is in meters
        get_fill_color=[255, 0, 0],
        get_line_color=[127, 0, 0],
        get_line_width=5,
        pickable=True,
        auto_highlight=True,
    )

    return layer, center


def plot(
    df: pd.DataFrame,
    kind: str,
    *,
    crs: str | None = None,
) -> str:
    match kind:
        case "timeline":
            layer, center = timeline_layer(df, crs)
        case "gps":
            layer, center = gps_layer(df, crs)
        case _:
            raise ValueError(f"Kind '{kind}' not supported.")

    # Set the viewport location
    view_state = pdk.ViewState(longitude=center.x, latitude=center.y, zoom=10)

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)

    return r.to_html()  # type: ignore
