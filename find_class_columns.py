# Find MySQL column names

import mysql.connector
import re

# Get the table columns names. A string has to be constructed that looks
# exactly like SQL query. This query is then sent to the MySQL server and the
# result is assigned to a variable with fetchall() function.
# An absolute name of the table is needed. From this name the database and table
# names can be obtained. 
def get_col_names(table_name):
    database = table_name.split('.')[0] # obtain database and table names
    table = table_name.split('.')[1]
    
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
    col_names = cursor.fetchall()

    # Transform the list from the fetchall() function to simple list of strings
    p_names = [re.sub(r'\(|\)|\'|,', '', str(x)) for x in col_names]

    conn.commit() # Send the query to MySQL
    print(p_names) 
    return p_names

# Build a table creating SQL query. This table will contain the results for
# each column(class column or non class column)
def table_create(table_name):
    new_table_name = str(table_name)+'_find_classes_2' # create name for the new
                                                     # tabble           
    mysql_send = '''
                CREATE TABLE %s(
                `column` VARCHAR(50),
                is_it_class VARCHAR(20),
                unique_percentage FLOAT
                ); 
                 ''' % new_table_name

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')
    cursor = conn.cursor()     # there are no results to fetch here because all
    cursor.execute(mysql_send) # the changes are made on the server side

    conn.commit()

# Build SQL query to insert data into the new table. Here besides the
# table name, column name is needed as well. 
def insert_found_classes(table_name, column_name):

    new_table_name = str(table_name)+'_find_classes_2'

    # this query uses some subqueries to calculate which columns are less than
    # 20 percent unique. These tables are considered classes because values
    # repeating 5 or more times
    mysql_insert = '''
        INSERT INTO %s(`column`, is_it_class, unique_percentage)
        SELECT \'%s\', (CASE
        WHEN
        ((WITH selection AS (SELECT DISTINCT %s FROM %s) SELECT COUNT(%s) FROM selection) / 
        (SELECT COUNT(%s) FROM %s)*100) < 20
        THEN 'class'
        ELSE 'Not a class'
        END) AS 'is_it_class', 
        ((WITH selection_2 AS (SELECT DISTINCT %s FROM %s) SELECT COUNT(%s) FROM selection_2) / 
        (SELECT COUNT(%s) FROM %s)*100) AS unique_percentage;
                  ''' % (new_table_name, column_name, column_name, table_name,
                         column_name, column_name, table_name, column_name,
                         table_name, column_name, column_name, table_name)

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')
    cursor = conn.cursor()
    cursor.execute(mysql_insert)

    conn.commit()
    print(mysql_insert)

# Create a function that calls all the functions.
# Furst, create the list with column names. Second,
# call the table creating function. Third, call the function that makes the
# calculations and inserts them into the new table. A loop is used to get
# every column name from the list we prepared one by one.
def all_func(table_name):
    c_names = get_col_names(table_name)
    table_create(table_name)
    for col_name in c_names:
        insert_found_classes(table_name, col_name)

def main():
    all_func('protein_data.protein_levels')

if __name__ == '__main__':
    main()




