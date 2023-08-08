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
header_written = False

# Keys to exclude from CSV
keys_to_exclude = ["chromosome2", "start2", "stop2", "representative_transcript2"]

# Check for 'records' and iterate through each record
if "records" in data:
    for record in data["records"]:
        group_id = record.get("id")  # Get the group ID from the record

        # Check if 'variants' is present and iterate through each variant
        if "variants" in record:
            for variant in record["variants"]:
                # If 'coordinates' is present and not empty, write to CSV
                if "coordinates" in variant and variant["coordinates"]:
                    coordinates = variant["coordinates"]
                    # Skip if the "chromosome" field is empty
                    if not coordinates.get("chromosome"):
                        continue

                    # Remove unwanted keys
                    coordinates = {k: v for k, v in coordinates.items() if k not in keys_to_exclude}

                    # Add group_id to the coordinates
                    coordinates["group_id"] = group_id

                    sys.stderr.write("Coordinates found:\n")
                    sys.stderr.write(json.dumps(coordinates, indent=4) + '\n')

                    # Write the CSV header if not already written
                    if not header_written:
                        writer.writerow(coordinates.keys())
                        header_written = True

                    # Write the CSV row
                    writer.writerow(coordinates.values())
