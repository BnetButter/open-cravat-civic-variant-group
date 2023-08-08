# open-cravat-civic-variant-group

This is a module that can be added to OpenCravat to allow annotation from CIVIC Variant Group data

The `civic_variant_group` is the actual module to be loaded into OpenCravat.

The `scripts` directory contains scripts that pulls data from CIVIC API and generates a sqlite3 database

To create the sqlite3 database from the `scripts` directory:

```bash
# Pull data from CIVIC variant group API
curl https://civicdb.org/api/variant_groups?count=9999 > civicdata.json

# Create the group table
python3 create_group.py < civicdata.json > 'group_table.csv'

# Create the variant table
python3 create_variants.py < civicdata.json > 'variant_table.csv'

# Create the sqlite3 database. Note that the names of the files are harded coded in
python3 create_sqlite3.py
```
