# treated or not-treated with drug mice comparisson

import mysql.connector
import re


def create_table(destination_table):
    # Create a table for the comparisson of the protein levels for memantin
    # injected mice versus non injected.
    
    create_t = '''
                CREATE TABLE %s(
                protein VARCHAR(15),
                AVG_non_injected FLOAT(8),
                AVG_injected_memantine FLOAT(8),
                percent_difference FLOAT(8)
                );
               ''' % destination_table

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')
    cursor = conn.cursor()
    cursor.execute(create_t)
    conn.commit()


def get_col_names(table_name):
    # Get the table columns names. A string has to be constructed that looks
    # exactly like SQL query. This query is then sent to the MySQL server and
    # the result is assigned to a variable with fetchall() function.
    # An absolute name of the table is needed. From this name the database
    # and table names can be obtained.
    
    database = table_name.split('.')[0] # obtain database names
    table = table_name.split('.')[1] # obtain table names
    
    get_c_names = ''' 
                  SELECT COLUMN_NAME
                  FROM INFORMATION_SCHEMA.COLUMNS
                  WHERE TABLE_SCHEMA = \'%s\'
                  AND
                  TABLE_NAME = \'%s\';
                  ''' % (database, table) # build the SQL query
    
    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance') # MySQL connection
    cursor = conn.cursor()
    cursor.execute(get_c_names)
    col_names = cursor.fetchall() # Get result from MySQL

    slice_names = col_names[1:-4]# slice out the columns not filled
                                 # with single protein values
    
    p_names = [re.sub(r'\(|\)|\'|,', '', str(x)) for x in slice_names]
        # Transform the list from the fetchall() function to simple
        # list of strings

    conn.commit() # Send the query to MySQL
    print(p_names) 
    return p_names


def populate_table(destination_table, protein_name):
    # Find the average protein levels by class(treated with memantine and
    # not treated). Find the percent difference between treated and not treated.
    
    populate = '''
                INSERT INTO %s(protein,
                AVG_non_injected, AVG_injected_memantine, percent_difference)

                VALUES(\'%s\', 
                (SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-SC-s'),

                (SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-SC-m'),

                (SELECT ((((SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-SC-s') - (SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-SC-m')) / 
                ((SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-SC-s') + (SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-SC-m')))*2)*100)
                );
               ''' % (destination_table, protein_name, protein_name, protein_name,
                      protein_name, protein_name, protein_name, protein_name)
    print(populate)

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')
    cursor = conn.cursor()
    cursor.execute(populate)
    conn.commit()

# call all the functions above. The 'populate_table()' function is called 77
# times in a loop for each column name.

def functions_call(table_name, destination_table):
    create_table(destination_table)    
    column_names = get_col_names(table_name)
    for name in column_names:
        populate_table(destination_table, name)

def main():
    functions_call('protein_data.protein_levels',
                   'protein_data.drug_percent_assessment')

if __name__ == '__main__':
    main()


