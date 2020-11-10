# Protein Groups
# This script uses the table 'protein_info.level_bins' created in the
# 'level.bins.sql' file 
import mysql.connector
import re


class prot_groups:

    def __init__(self, table_name):
        self.table_name = table_name # Make the table name usable for all the
                                     # the class.
        
    def get_col_names(self, main_column):
        # Get column names from the bins average column.
        self.main_column = main_column

        database = self.table_name.split('.')[0]
        table = self.table_name.split('.')[1]
        
        get_c_names = '''
                      SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA = \'%s\'
                      AND
                      TABLE_NAME = \'%s\';
                      ''' % (database, table)

        
        conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                       password = 'dance')
        cursor = conn.cursor()
        cursor.execute(get_c_names)
        col_names = cursor.fetchall()

        p_names = [re.sub(r'\(|\)|\'|,', '', str(x)) for x in col_names]
        if main_column in p_names:
            p_names.pop(p_names.index(main_column))

        self.p_names = p_names

        conn.commit()
        print(p_names)
        

    def find_similarity(self, similarity_table, matching_column):
        # Find the average protein columns which levels synchronize with the
        # main column 'DYRK1A_N'. Columns with lowest average result where
        # 'DYRK1A_N' has it's lowest at 1. Then the higher levels of 'DYRK1A_N'
        # has to match the exat same level of the other protein. 
        
        similarity_check = '''
        INSERT INTO %s(protein_couple, Similarity)
        VALUES('%s - %s', 
	(SELECT (CASE
        WHEN
        (SELECT %s FROM %s WHERE %s = 1)
        < (SELECT %s FROM %s WHERE %s = 2)
        
        < (SELECT %s FROM %s WHERE %s = 3)
        < (SELECT %s FROM %s WHERE %s = 4)
        THEN 'Yes' # When we have similarity at all the 4 ranges.
        ELSE 'No' # When one or more of the ranges are in different position.
        END))
        );
        ''' % (similarity_table, self.main_column, matching_column[4:],
               matching_column, self.table_name, self.main_column,
               matching_column, self.table_name, self.main_column,
               matching_column, self.table_name, self.main_column,
               matching_column, self.table_name, self.main_column,)
        print(similarity_check)

        conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                       password = 'dance')
        cursor = conn.cursor()
        cursor.execute(similarity_check)
        conn.commit()

def call_methods():
    # Call the class methods.
    protein_object = prot_groups('protein_info.level_bins')
    protein_object.get_col_names('DYRK1A_N')
    for avg_protein in protein_object.p_names:
        protein_object.find_similarity('protein_info.protein_similarity',
                                       avg_protein)
    
if __name__ == '__main__':
    call_methods()

