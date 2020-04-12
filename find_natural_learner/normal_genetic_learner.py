# Find a natural learner

# In the protein data (https://www.kaggle.com/ruslankl/mice-protein-expression)
# table we  have protein levels divided by class. One of the classes is
# called 'stimulated to learn'. The average protein levels for the stimulated
# to learn mouse will be compared with the average protein levels for every
# normal mouse. The mouse which has protein levels closest to the stimulated
# to learn levels is our natural learner.


import mysql.connector
import re

def mouse_id(source_table):
    # Find the MiceID of the mice which are normal and not_stimulated
    
    send_sql = '''
                SELECT SUBSTRING_index(MouseID, '_', 1)
                FROM %s
                WHERE class = 'c-SC-s'
                GROUP BY SUBSTRING_INDEX(MouseID, '_', 1);
               ''' % source_table
    
    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')# Change this with your
                                                      # password
    cursor = conn.cursor()
    cursor.execute(send_sql)
    individual_mouse = cursor.fetchall()
    conn.commit()

    m_names = [re.sub(r'\(|\)|\'|,', '', str(x)) for x in individual_mouse]
    # Remove unnecessary symbols from the list with 're' module.
    
    return m_names


def create_table(source_table, destination_table):
    # Create a table for the comparisson of the protein levels for memantin
    # injected mice versus non injected.

    m_id = mouse_id(source_table)
    m_form = ['normal_mouse_'+x+' FLOAT(8)' for x in m_id]
    str_form = str(m_form)
    add_to_table = re.sub(r'\[|\]|\'', '', str_form)
    # Transform the unique MouseID numbers into parts of SQL expression.
    
    create_t = '''
                CREATE TABLE %s(
                protein VARCHAR(15),
                AVG_normal FLOAT(8),
                AVG_stimulated FLOAT(8),
                percent_difference FLOAT(8),
                %s
                );''' % (destination_table, add_to_table)
    # Build table creating SQL query to execute in MySQL.

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')
    # Create connection with MySQL server.
    
    cursor = conn.cursor()
    cursor.execute(create_t)
    conn.commit()
    # Start the query execution in MySQL

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
    return p_names


def populate_table(destination_table, protein_name):
    # Populate the new table with data for the average protein levels for all
    # normal and stimulated mice and for the normal individual mouse.

    em_id = mouse_id('protein_data.protein_levels')
    col_insert = ['normal_mouse_'+x for x in em_id]
    str_col_insert = str(col_insert)
    sub_col = re.sub(r'\'|\[|\]', '', str_col_insert)
    # Transform the unique MouseID numbers into parts of SQL expression.
    
    ext_mouse_id = ["""(SELECT AVG(%s) FROM protein_data.protein_levels WHERE MouseID REGEXP \'^""" 
                    +x+'\')' for x in em_id]
    # Create expression that finds the average expression level of a protein
    # in every normal mouse

    str_mid = str(ext_mouse_id)
    str_mid_sub = re.sub(r'\[|\]|\"', '', str_mid)
    str_mid_sub = str_mid_sub % (protein_name, protein_name, protein_name,
                                   protein_name, protein_name)
    # Clear the expression from the unnecessary characters.
    
    populate = '''
                INSERT INTO %s(protein,
                AVG_normal, AVG_stimulated, percent_difference, %s)

                VALUES(\'%s\', 
                (SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-SC-s'),

                (SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-CS-s'),

                (SELECT ((((SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-CS-s') - (SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-SC-s')) / 
                ((SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-CS-s') + (SELECT AVG(%s) FROM protein_data.protein_levels
                WHERE class = 'c-SC-s')))*2)*100),

                %s
                );
               ''' % (destination_table, sub_col, protein_name, protein_name,
                      protein_name, protein_name, protein_name, protein_name,
                      protein_name, str_mid_sub)
    # Put the whole SQL expression together with all it's variables.
    
    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance') # MySQL connection

    cursor = conn.cursor()
    cursor.execute(populate)
    conn.commit() # Send the query to MySQL.


def functions_call(table_name, destination_table):
    # Call all the functions in the proper sequence. Get the unique codes for
    # every normal mouse in the research. Create the table for the data of
    # the comparisson of the average protein levels for normal and stimulated
    # to learn mice. Insert a row of agregate data for each protein.

    mouse_id(table_name)
    create_table(table_name, destination_table)    
    column_names = get_col_names(table_name)
    for name in column_names:
        populate_table(destination_table, name)

def main():
    # Create a function that calls tha main function

    functions_call('protein_data.protein_levels',
                   'protein_data.find_natural_learner')


if __name__ == '__main__':
    main()






