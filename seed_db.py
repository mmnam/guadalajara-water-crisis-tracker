import argparse
from pathlib import Path
from database.seed import seed

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import demo or curated historical records')
    parser.add_argument('--file', type=Path, help='JSON records matching data/seed_data.json')
    args = parser.parse_args()
    seed(args.file)
    print('Database initialized. Existing records preserved.')
