from manager.dataset import Dataset

assets = [
    "assets/lowbid_manche_demo.csv",
    "assets/lowbid_multi_manches_500x40.csv",
    "assets/lowbid_stress_200k.csv"
]

datasets = []

for file_path in assets:
    datasets.append(Dataset(name="Sample Dataset", file_path=file_path))

if len(datasets) == 0:
    print("No datasets loaded.")