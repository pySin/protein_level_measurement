# Protein level distribution
import mysql.connector
import re


## Make Destination Table

def table_create(destination_table):
    # make a table to contain the values from the protein fluctuations
    # analysis
    table_create = """
                    CREATE TABLE %s(
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    MouseID VARCHAR(15),
                    protein VARCHAR(40),
                    MIN FLOAT(5),
                    MAX FLOAT(5),
                    fluctuations_range FLOAT(5),
                    lower_third_count TINYINT,
                    middle_third_count TINYINT,
                    upper_third_count TINYINT,
                    class VARCHAR(15)
                    );
                   """ % destination_table # this query is to be sent to MySQL

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance') # Make MySQL connection
    cursor = conn.cursor()
    cursor.execute(table_create)
    conn.commit() # send the query for execution


def fluctuations(source_table, destination_table, mouse_id, protein):
    # Create a long MySQL query that manipulates data from 'protein_levels'.
    # The fluctuations range for single protein in single mouse is devided in
    # three sections(lower, middle and upper). This will help in creating
    # a 'protein fluctuations profile'. This profile then could be used for
    # other analysis. In the 'lower_third_count' column we store the protein
    # levels from the lowest result to 1/3 of the range to the highest result.
    # 2/3(middle) and 3/3(upper) have a third of the range as well.

    populate = """
            INSERT INTO %s(MouseID, protein, MIN,
            MAX, fluctuations_range, lower_third_count, middle_third_count,
	    upper_third_count, class)
      SELECT MouseID, \'%s\', MIN(%s), MAX(%s),
             (MAX(%s) - MIN(%s)),
      
      (SELECT COUNT(%s) FROM %s
			WHERE %s BETWEEN 
                        (SELECT MIN(%s) FROM %s
                        WHERE MouseID REGEXP \'^%s\')
			AND
			(SELECT MIN(%s)
			+ ( (MAX(%s) - MIN(%s))/3 )
			FROM %s 
                        WHERE MouseID REGEXP '^%s')
			AND 
	  MouseID REGEXP '^%s'),
      
      (SELECT COUNT(%s) FROM %s
			WHERE %s BETWEEN 
                        (SELECT MIN(%s) + ( (MAX(%s)
                        - MIN(%s))/3 ) FROM %s 
                        WHERE MouseID REGEXP '^%s')
			AND 
			(SELECT MIN(%s) + ( (MAX(%s)
			- MIN(%s))/3 ) + ( (MAX(%s)
			- MIN(%s))/3 )
                        FROM %s
                        WHERE MouseID REGEXP '^%s')
			AND
	  MouseID REGEXP '^%s'),
      
      (SELECT COUNT(%s) FROM %s
			WHERE %s BETWEEN 
                        (SELECT MIN(%s) + ( (MAX(%s)
                        - MIN(%s))/3 ) + ( (MAX(%s) - MIN(%s))/3 )
                        FROM %s
                        WHERE MouseID REGEXP '^%s')
			AND 
			(SELECT MAX(%s)
                        FROM %s
                        WHERE MouseID REGEXP '^%s')
			AND 
	  MouseID REGEXP '^%s'),

	  class
      
        FROM %s
        WHERE MouseID REGEXP '^%s'; 
               """ % (destination_table, protein, protein, protein, protein,
                      protein, protein, source_table, protein, protein,
                      source_table, mouse_id, protein, protein, protein,
                      source_table, mouse_id, mouse_id, protein, source_table,
                      protein, protein, protein, protein, source_table,
                      mouse_id, protein, protein, protein, protein, protein,
                      source_table, mouse_id, mouse_id, protein, source_table,
                      protein, protein, protein, protein, protein, protein,
                      source_table, mouse_id, protein, source_table, mouse_id,
                      mouse_id, source_table, mouse_id
                     ) # Fill in the new created table with data

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')#Create MySQL connection.
    cursor = conn.cursor()
    cursor.execute(populate)
    conn.commit() # Send the query for execution.


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

    conn.commit() # Send the query for execution
    return p_names


def mouse_codes(source_table):
    # There are 77 different mouse and there is a different code(MouseID) for
    # each mouse. All 72 proteins has to be analysed for each mouse.
    # 77*72=5544 rows of results

    send_query = '''
                SELECT SUBSTRING_INDEX(MouseID, '_', 1)
                FROM %s
                GROUP BY SUBSTRING_INDEX(MouseID, '_', 1);
                 ''' % source_table

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance') # MySQL connection

    cursor = conn.cursor()
    cursor.execute(send_query)
    mouse_codes = cursor.fetchall() # get the results from MySQL

    mouse_codes = [re.sub(r'\(|\)|\'|,', '', str(x)) for x in mouse_codes]
                  # Cler the results from the unnecessary characters.
    conn.commit() # Send the query for execution.
    return mouse_codes


def function_call(destination_table, source_table):
    # Call al the functions in the desired order - create table, create a list
    # with the unique mouse codes, create a list with the unique mouse ID's,
    # create 2 loops to combine each MouseID with each protein. Send the
    # queries to MySQL for execution with 'fluctuations()' function.
    
    table_create(destination_table)
    single_mouse_codes = mouse_codes(source_table)
    column_names = get_col_names(source_table)
    
    for mouse_id in single_mouse_codes:
        for protein in column_names:
            fluctuations(source_table, destination_table, mouse_id, protein)
            print(mouse_id) # Print the MouseID just to check if the proces
                            # is running well.

def main():
    function_call('protein_data.protein_fluctuations_5',
                  'protein_data.protein_levels')

if __name__ == '__main__':
    main()











