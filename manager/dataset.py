import csv

class Dataset:
    def __init__(self, name, file_path):
        self.name = name

        if not file_path.endswith('.csv'):
            raise ValueError("File path must end with '.csv'")
        
        with open(file_path, 'r') as f:
            self.data = list(csv.reader(f, delimiter=','))