import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        """
        Set up data sources. 
        Cravat will automatically make a connection to 
        data/example_annotator.sqlite using the sqlite3 python module. The 
        sqlite3.Connection object is stored as self.dbconn, and the 
        sqlite3.Cursor object is stored as self.cursor.
        """
        pass
    
    def annotate(self, input_data, secondary_data=None):
        """
        The annotator parent class will call annotate for each line of the 
        input file. It takes one positional argument, input_data, and one
        keyword argument, secondary_data.
        
        input_data is a dictionary containing the data from the current input 
        line. The keys depend on what what file is used as the input, which can 
        be changed in the module_name.yml file. 
        Variant level includes the following keys: 
            ('uid', 'chrom', 'pos', 'ref_base', 'alt_base')
        Variant level crx files expand the key set to include:
            ('hugo', 'transcript','so','all_mappings')
        Gene level files include
            ('hugo', 'num_variants', 'so', 'all_so')
        
        secondary_data is used to allow an annotator to access the output of
        other annotators. It is described in more detail in the CRAVAT 
        documentation.
        
        annotate should return a dictionary with keys matching the column names
        defined in example_annotator.yml. Extra column names will be ignored, 
        and absent column names will be filled with None. Check your output
        carefully to ensure that your data is ending up where you intend.
        """


        chrom, pos, ref_base, alt_base = input_data['chrom'], input_data['pos'], input_data['ref_base'], input_data['alt_base']
        query = """
        SELECT Variants.*, VariantGroups.name, VariantGroups.description
        FROM Variants
        JOIN VariantGroups ON Variants.group_id = VariantGroups.id
        WHERE Variants.chromosome = ? AND Variants.start = ? AND Variants.reference_bases = ? AND Variants.variant_bases = ?
        """

        chrom = chrom.replace("chr", "")

        # Execute the query with the provided variables
        self.cursor.execute(query, (chrom, pos, ref_base, alt_base))

        # Fetch the result
        result = self.cursor.fetchone()

        
        out = {}

        # Check if a result was found
        if result:
            # Process the result
            # Example: print the result
            
            name = result[9]
            descr = result[10]

            out["name"] = name
            out["description"] = descr

        return out
    
    def cleanup(self):
        """
        cleanup is called after every input line has been processed. Use it to
        close database connections and file handlers. Automatically opened
        database connections are also automatically closed.
        """
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()