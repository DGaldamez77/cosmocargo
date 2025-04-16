import json, sys, datetime
from dataaccess import db

def read_json_from_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    
    except FileNotFoundError:
        print("File not found: ", file_path)
    except json.JSONDecodeError:
        print("Invalid JSON format in file: ", file_path)

if __name__ == "__main__":
    print(f"\n=============================================")
    print("job started at " + str(datetime.datetime.now(datetime.timezone.utc)))
    print(f"=============================================")

    if len(sys.argv) <= 1:
        print("missing file name as command line argument")
        sys.exit(1)

    file_name = sys.argv[1]
    data = read_json_from_file(file_name)
    if data == None:
        sys.exit(1)

    print("file read... starting to process")
    db.write_to_db(data['shipments'])
    