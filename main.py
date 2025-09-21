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
    map_df = pd.read_csv("goodnature_analysis/seeds/nz_suburb_locality.csv")
    nz_addresses_df = pd.read_csv("goodnature_analysis/seeds/nz_addresses.csv")

    territorial_authorities = nz_addresses_df["territorial_authority"].dropna().unique()
    territorial_suburbs = {territory: nz_addresses_df[nz_addresses_df["territorial_authority"] == territory]["suburb_locality"].dropna().unique().tolist() for territory in territorial_authorities}

    with open('streamlit_app/data/territorial_suburbs.json', 'w') as f:
        json.dump(territorial_suburbs, f, indent=4)

    map_df["coordinates"] = map_df["WKT"].apply(wkt_to_coordinates)
    map_df = map_df[["id", "parent_id","name","type","start_date","name_ascii", "coordinates"]]
    map_df["parent_id"] = map_df["parent_id"].fillna(0).astype(int)

    for territory in territorial_authorities:
        territory_map_df = map_df[map_df["name"].isin(territorial_suburbs[territory])]

        # map_df.to_json("streamlit/data/nz_suburbs_map.json", orient="records")
        locations = [{'type': 'Feature',
            'properties': {
            'id': row["id"],
            'parent_id': row['parent_id'],
            'name': row['name'],
            'type': row['type'],
            'start_date': row['start_date'],
            'name_ascii': row['name_ascii']},
            'geometry': {'type': 'Polygon',
            'coordinates': row["coordinates"]},
            'id': f'{row["id"]}'
        } for _, row in territory_map_df.iterrows()]
        map_dict = {'type': 'FeatureCollection', 'features': locations}
        with open(f'streamlit_app/data/nz_{territory}_map.json', 'w') as f:
            json.dump(map_dict, f, indent=4)

def main():
    print("Loading file")
    model()

if __name__ == "__main__":
    main()
