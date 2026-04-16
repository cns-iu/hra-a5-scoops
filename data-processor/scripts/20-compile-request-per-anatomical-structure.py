from shared import *

heart_dict = {
    "interventricular septum": "VH_F_interventricular_septum",
    "left cardiac atrium": "VH_F_left_cardiac_atrium",
    "right cardiac atrium": "VH_F_right_cardiac_atrium",
    "heart left ventricle": "VH_F_left_ventricle",
    "heart right ventricle": "VH_F_right_ventricle",
    "Posteromedial head of posterior papillary muscle of left ventricle": "VH_F_papillary_muscle_of_heart_posmed",
}


def load_data():
    df = pd.read_csv("data/cell_types_in_anatomical_structurescts_per_as.csv")
    print(df)
    return df


def get_distribution(df: pd.DataFrame, as_label: str):

    # Filter first
    filtered_df = df[
        (df["organ"] == "heart")
        & (df["sex"] == "Female")
        & (df["tool"] == "azimuth")
        & (df["as_label"] == as_label)
    ].copy()

    # Choose top N
    N = 9  # change this to whatever you want

    top_cell_types = filtered_df["cell_percentage"].value_counts().nlargest(N).index

    # Replace others with 'OTHER'
    filtered_df["cell_label"] = filtered_df["cell_label"].where(
        filtered_df["cell_percentage"].isin(top_cell_types), "OTHER"
    )
    print(filtered_df)

    # transform
    initial_dict = filtered_df.groupby("cell_label")["cell_percentage"].sum().to_dict()

    rounded_dict = {
        k: round(v, 2) if isinstance(v, (int, float)) else v
        for k, v in initial_dict.items()
    }

    # rounded_dict.pop("OTHER")

    print(rounded_dict)

    return rounded_dict


def make_3d_mesh_request(file_subpath: str, num_nodes, distribution):
    output_file = f"output/{file_subpath}.json"

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    mesh_3d_api_url = "https://apps.humanatlas.io/api/v1/mesh-3d-cell-population"

    payload = {
        "file": "https://cdn.humanatlas.io/digital-objects/ref-organ/heart-female/v1.3/assets/3d-vh-f-heart.glb",
        "file_subpath": file_subpath,
        "num_nodes": num_nodes,
        "node_distribution": distribution,
    }

    headers = {"Content-Type": "application/json"}
    print(json.dumps(payload, indent=2))

    response = requests.post(mesh_3d_api_url, json=payload, headers=headers)

    if response.status_code == 200:
        with open(output_file, "w") as f:
            f.write(response.text)
        print(f"Success. Saved to {output_file}")
    else:
        print(f"Failed: {response.status_code}")
        print(response.text)


def main():
    df = load_data()

    for key in heart_dict:
        distribution = get_distribution(df, key)
        make_3d_mesh_request(heart_dict[key], 6000, distribution)


if __name__ == "__main__":
    main()
