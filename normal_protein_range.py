# Find normal protein ranges for mice
import mysql.connector
import re
import empty_to_null


def p_range_table(table_name, new_table_name):
    # Create a table to fit the data from the minimum and the maximum
    # of protein concentrations per type of mouse(exmp. The biggest value
    # of 'DYRK1A_N' for all the normal, non-stimulated mice, injected with
    # memantin). 
    
    create_table = '''
                CREATE TABLE %s(
                protein VARCHAR(50),
                class_min FLOAT(8),
                class_max FLOAT(8),
                Genotype VARCHAR(50),
                Treatment VARCHAR(50),
                behavior VARCHAR(50),
                class VARCHAR(50)
                );
                   ''' % new_table_name

    print(create_table)
    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'your_password') # MySQL connection
    cursor = conn.cursor()
    cursor.execute(create_table)
    conn.commit() # Send the query to MySQL

 
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
                                   password = 'your_password') # MySQL connection
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


def class_codes(table_name, column_name):
    # Get class names from the 'class' column of the data
    get_class_names = '''
                    SELECT %s FROM %s
                    GROUP BY %s;
                      ''' % (column_name, table_name,
                             column_name) # Build the SQL query.

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'your_password') # MySQL connection
    cursor = conn.cursor()
    cursor.execute(get_class_names)
    class_fetch = cursor.fetchall()

    class_names = [re.sub(r'\(|\)|\'|,', '', str(x)) for x in class_fetch]

    conn.commit() # Send the query to MySQL.
    # print(class_names) 
    return class_names    


def range_protein(table_name, new_table_name, class_column):
    # Call all the above functions.

    empty_to_null.empty_to_null(table_name) # External file is called to
        # change the empty values to NULL in the source table. The empty
        # values are changed because they generate an error.
    p_range_table(table_name, new_table_name)
    column_names = get_col_names(table_name)
    get_classes = class_codes(table_name, class_column) # the 'class_column'
        # is the class inside which MIN and MAX are searched for

    for protein_name in column_names:
        for class_name in get_classes:
            
            min_max = '''
                    INSERT INTO %s(protein,
                    class_min, class_max, Genotype, Treatment,
                    Behavior, class)
                    SELECT \'%s\' AS 'protein', MIN(%s) AS 'class_min',
                    MAX(%s) AS 'class_max', Genotype, Treatment, Behavior, class
                    FROM  %s
                    WHERE class = \'%s\';
                      ''' % (new_table_name, protein_name, protein_name,
                             protein_name, table_name, class_name) # Build MySQL
                # query from all the variables generated  by the functions
                # called above

            conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'your_password') # MySQL connection.
            cursor = conn.cursor()
            cursor.execute(min_max)
            print(min_max)
            conn.commit()


def main():
    range_protein('protein_data.protein_levels',
                  'protein_data.protein_min_max_2', 'class')

if __name__ == '__main__':
    main()







