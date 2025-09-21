import pandas as pd

def space_to_bracket(pair: str):
    pair = pair.replace(" ", ", ")
    return f"[{pair}]"


def wkt_to_coordinates(wkt_value: str):
    wkt_value = wkt_value.replace("MULTIPOLYGON (((", "").replace(")))", "")
    val_pairs = wkt_value.split(",")
    bracket_pairs = ", ".join([space_to_bracket(pair) for pair in val_pairs])
    return f"[[{bracket_pairs}]]"


def model(dbt, session):
    map_df = dbt.ref("nz_suburb_locality")
    map_df["coordinates"] = map_df["geometry"].apply(wkt_to_coordinates)
    map_df = map_df[["id", "parent_id","name","type","start_date","name_ascii", "coordinates"]]
    return map_df
