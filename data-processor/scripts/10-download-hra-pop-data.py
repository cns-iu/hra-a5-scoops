from shared import *


def download_data():

    url = "https://apps.humanatlas.io/api/grlc/hra-pop/cell_types_in_anatomical_structurescts_per_as.csv"
    output_dir = "data"
    output_file = os.path.join(
        output_dir, "cell_types_in_anatomical_structurescts_per_as.csv"
    )

    # Create data directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    response = requests.get(url)

    if response.status_code == 200:
        with open(output_file, "w") as f:
            f.write(response.text)
        print(f"Download successful. Saved to {output_file}")
    else:
        print(f"Failed to download. Status code: {response.status_code}")


def main():
    download_data()


if __name__ == "__main__":
    main()
