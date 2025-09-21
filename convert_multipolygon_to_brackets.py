import pandas as pd
import json

def space_to_bracket(pair: str):
    values = pair.split(" ")
    return [float(values[0]), float(values[1])]

def wkt_to_coordinates(wkt_value: str):
    wkt_value = wkt_value.replace("MULTIPOLYGON ", "").replace(")", "").replace("(", "")
    val_pairs = wkt_value.split(",")
    coordinates = [space_to_bracket(pair) for pair in val_pairs]
    return [coordinates]

def model():

    nz_territories_df = pd.read_csv("goodnature_analysis/seeds/territorial_authority_2025.csv")

    nz_territories_df["coordinates"] = nz_territories_df["WKT"].apply(wkt_to_coordinates)
    nz_territories_df = nz_territories_df[["TA2025_V1_00", "TA2025_V1_00_NAME", "TA2025_V1_00_NAME_ASCII", "LAND_AREA_SQ_KM", "AREA_SQ_KM", "SHAPE_Length", "coordinates"]]


    # map_df.to_json("streamlit/data/nz_suburbs_map.json", orient="records")
    territorial_authorities_boundaries = [{'type': 'Feature',
        'properties': {
        'territorial_id': row["TA2025_V1_00"],
        'territorial_name': row['TA2025_V1_00_NAME'],
        'territorial_name_ascii': row['TA2025_V1_00_NAME_ASCII'],
        'land_area_sq_km': row['LAND_AREA_SQ_KM'],
        'area_sq_km': row['LAND_AREA_SQ_KM'],
        'shape_length': row['SHAPE_Length']},
        'geometry': {'type': 'Polygon',
        'coordinates': row["coordinates"]},
        'id': f'{row["TA2025_V1_00"]}'
    } for _, row in nz_territories_df.iterrows()]
    map_dict = {'type': 'FeatureCollection', 'features': territorial_authorities_boundaries}
    with open(f'streamlit_app/data/nz_territorial_boundary_map.json', 'w') as f:
        json.dump(map_dict, f, indent=4)

def main():
    print("Loading file")
    model()

if __name__ == "__main__":
    main()
