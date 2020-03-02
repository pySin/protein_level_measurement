# Average Protein Concentration
import mysql.connector
import re


# Get the table columns names. A string has to be constructed that looks
# exactly like SQL query. This query is then sent to the MySQL server and the
# result is assigned to a variable with fetchall() function.

def get_col_names(database, table):

    get_c_names = """
                  SELECT COLUMN_NAME
                  FROM INFORMATION_SCHEMA.COLUMNS
                  WHERE TABLE_SCHEMA = \'%s\'
                  AND
                  TABLE_NAME = \'%s\';
                  """ % (database, table)

    # return get_c_names
    
    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')
    cursor = conn.cursor()
    cursor.execute(get_c_names)
    col_names = cursor.fetchall()

    conn.commit()
    return col_names

# The result is a list of tuples but what we need is a list of strings(column
# names). The function clear_names() removes the unwanted characters. 

def clear_names():
    col_names = get_col_names('your_database_1', 'your_table_1')

    p_names = [re.sub(r'\(|\)|\'|,', '', str(x)) for x in col_names]
    return p_names

# A function that receives a column name and creates an INSERT query to
# analyze the average levels of single protein when a mouse is treated with
# memantine drug.

def insert_query(protein):
    ins_query = """
    INSERT INTO your_database_2.your_table_2(Protein, avg_memantine, avg_saline)
    VALUES(\'%s\',

    (SELECT AVG(%s) FROM your_database_1.your_table_1
    WHERE Treatment = 'Memantine'),

    (SELECT AVG(%s) FROM your_database_1.your_table_1
    WHERE Treatment = 'Saline')
    );
                """ % (protein, protein, protein)

    print(ins_query)
    conn = mysql.connector.connect(host = 'localhost', user = 'root',
                                   password = 'dance')
    cursor = conn.cursor()
    cursor.execute(ins_query)

    conn.commit()

# create a functon that runs insert_query() function for each protein name in
# the list we created above

def main():
    clear_list = clear_names()
    for item in clear_list:
        insert_query(item)


if __name__ == '__main__':
    main()

