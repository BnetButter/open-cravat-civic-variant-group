import json
import csv
import sys

# Read JSON from stdout
json_string = sys.stdin.read()

# Parse the JSON string
try:
    data = json.loads(json_string)
except json.JSONDecodeError as e:
    sys.stderr.write(f"An error occurred while parsing JSON: {e}\n")
    sys.exit(1)

# Create a CSV writer object for stdout
writer = csv.writer(sys.stdout)

# Write the CSV header
writer.writerow(["id", "name", "description"])

# Check for 'records' and iterate through each record
if "records" in data:
    for record in data["records"]:
        record_id = record.get("id")
        name = record.get("name")
        description = record.get("description")

        # Write the CSV row
        writer.writerow([record_id, name, description])
