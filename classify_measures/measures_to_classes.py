# MySQL measures to quarter classes.

#The task is to substitute the protein values with the range quarter they fall
#under. The range between the minimum and the maximum level for each protein is
#divided in 4 quarters. Each protein can fall under the 1st, 2nd, 3rd or the
#4th quarter. In this way the numeric values are transformed into classes.


import mysql.connector
import re


def get_col_names(table_name):
    # Get column names from a table.

    database = table_name.split('.')[0]
    table = table_name.split('.')[1]
    
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

    conn.commit()
    return p_names


def remove_classes(table_name):
    # Remove the non-numeric column names.
    
    column_names = get_col_names(table_name)
    classes = ['Behavior', 'Genotype', 'Treatment', 'class', 'MouseID']

    for item in column_names:
        if item in classes:
            column_names.remove(item)

    return column_names


def calculate_1_protein(protein):
    # Build SQL query.
    # Create range of values for the protein levels. Get the minimum and
    # the maximum value for each protein and the range between these 2
    # numbers is devided in four. So we create 4 ranges: 1 - from the
    # minimum to the minimum+first quarter, 2 - from the
    # minimum+first quarter to minimum+second quarter and so on.

    in_string = '''
    (SELECT (CASE
    WHEN %s BETWEEN (SELECT MIN(%s) FROM protein_info.protein_levels) 
    AND (SELECT MIN(%s) FROM protein_info.protein_levels) 
    + ((SELECT MAX(%s) FROM protein_info.protein_levels)
    - (SELECT MIN(%s) FROM protein_info.protein_levels))*0.25
    THEN 'Quarter_1'
    WHEN %s 
    BETWEEN 
    ((SELECT MIN(%s) FROM protein_info.protein_levels) 
    + ((SELECT MAX(%s) FROM protein_info.protein_levels)
    - (SELECT MIN(%s) FROM protein_info.protein_levels))*0.25)
    AND 
    ((SELECT MIN(%s) FROM protein_info.protein_levels) 
    + ((SELECT MAX(%s) FROM protein_info.protein_levels)
    - (SELECT MIN(%s) FROM protein_info.protein_levels))*0.50)
    THEN 'Quarter_2'
                    
    WHEN %s 
    BETWEEN 
    ((SELECT MIN(%s) FROM protein_info.protein_levels) 
    + ((SELECT MAX(%s) FROM protein_info.protein_levels)
    - (SELECT MIN(%s) FROM protein_info.protein_levels))*0.50)
    AND 
    ((SELECT MIN(%s) FROM protein_info.protein_levels) 
    + ((SELECT MAX(%s) FROM protein_info.protein_levels)
    - (SELECT MIN(%s) FROM protein_info.protein_levels))*0.75)
    THEN 'Quarter_3'

    WHEN %s 
    BETWEEN 
    ((SELECT MIN(%s) FROM protein_info.protein_levels) 
    + ((SELECT MAX(%s) FROM protein_info.protein_levels)
    - (SELECT MIN(%s) FROM protein_info.protein_levels))*0.75)
    AND 
    ((SELECT MIN(%s) FROM protein_info.protein_levels) 
    + ((SELECT MAX(%s) FROM protein_info.protein_levels)
    - (SELECT MIN(%s) FROM protein_info.protein_levels))*1)
    THEN 'Quarter_4'
                    
    ELSE 'Error Record'
    END) AS \'%s\'),
                ''' % (protein, protein, protein, protein, protein, protein,
                       protein, protein, protein, protein, protein, protein,
                       protein, protein, protein, protein, protein, protein,
                       protein, protein, protein, protein, protein, protein,
                       protein, protein, protein)

    return in_string


def measure_to_class(table_name):
    # Combine 2 strings to form the final SQL like layout of the string.

    column_names = remove_classes(table_name) 
    str_column_names = re.sub(r'\[|\]|\'', '', str(column_names))
    # Remove the unnecessary characters from string.
    
    accumulate = '''

                 '''
    # Create an empty srting to join the SQL expressions for each protein
    # quarter range. 

    for item in column_names:
        accumulate = ''.join([accumulate, calculate_1_protein(item)])
    # Run 'calculate_1_protein()' function for each protein and join the
    # resulting string to 'accumulate' variable.

    send_query = '''
    INSERT INTO protein_info.protein_quarters(MouseID, %s,  
                                              Genotype, Treatment, Behavior)
    SELECT MouseID, 
    %s

    Genotype, Treatment, Behavior 
    FROM protein_info.protein_levels;
                 ''' % (str_column_names, accumulate)
    # Put together the whole SQL query string.
    

    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')
    cursor = conn.cursor()
    cursor.execute(send_query)
    conn.commit()
    # Create MySQL connection and run the query.
    

if __name__ == '__main__':
    measure_to_class('protein_info.protein_levels')

     


