import sqlite3
import csv

# Connect to the SQLite database (will create if not exists)
conn = sqlite3.connect("civic_variant_group.sqlite")
cursor = conn.cursor()

# Create "VariantGroups" table
cursor.execute("""
CREATE TABLE IF NOT EXISTS VariantGroups (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT
)
""")

# Load data from "group_table.csv" into "VariantGroups" table
with open("group_table.csv", 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        cursor.execute("INSERT INTO VariantGroups (id, name, description) VALUES (?, ?, ?)", row)

# Create "Variants" table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Variants (
    chromosome TEXT,
    start INTEGER,
    stop INTEGER,
    reference_bases TEXT,
    variant_bases TEXT,
    representative_transcript TEXT,
    ensembl_version INTEGER,
    reference_build TEXT,
    group_id INTEGER,
    FOREIGN KEY(group_id) REFERENCES VariantGroups(id)
)
""")

# Load data from "group_variants.csv" into "Variants" table
with open("group_variants.csv", 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        cursor.execute("INSERT INTO Variants (chromosome, start, stop, reference_bases, variant_bases, representative_transcript, ensembl_version, reference_build, group_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

# Commit the changes and close the connection
conn.commit()
conn.close()
