# Change the empty string values to NULL in MySQL
import mysql.connector
import re


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


    p_names = [re.sub(r'\(|\)|\'|,', '', str(x)) for x in col_names]
        # Transform the list from the fetchall() function to simple
        # list of strings

    conn.commit() # Send the query to MySQL
    print(p_names) 
    return p_names


def empty_to_null(table_name):
    # Check every column in the source table for empty values and if found
    # change them to NULL. The column names are available from the function
    # above. This function is called in the main script
    # 'normal_protein_range.py'
    column_names = get_col_names(table_name)
    for column_name in column_names:    
        send_query = '''
                    UPDATE %s
                    SET %s = NULL
                    WHERE %s = '';
                     ''' % (table_name, column_name, column_name)

        conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance') # MySQL connection
        cursor = conn.cursor()
        cursor.execute(send_query)
        conn.commit() 
