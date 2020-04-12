# Protein Level Measurement

## Introduction
Analyse data from protein levels in the nuclear fraction of cerebral cortex in mice. The data is available at: https://www.kaggle.com/ruslankl/mice-protein-expression. The experiment uses different strategies to assess associative learning explained in the link provided. 

## Tasks

1. Compare the average levels of every protein when the mice are injected with mematine drug or not. / Done ('avg_protein_levels.py')
2. Compare the expression variations of single protein in single normal mouse. / Done ('protein_level_variations.sql')
3. Find which columns are class columns in a table. / Done ('find_class_columns.py')
4. Change the empty value cells to NULL. / Done (empty_to_null.py)
5. Find minimum and maximum levels of protein in the scope of a class. / Done ('normal_protein_range.py')
6. Assess drug effect by comparing treated and not treated mice protein levels. / Done ('drug_assessment.py')
7. Create protein fluctuations profile for each mouse for each protein. /Done ('protein_fluctuations/p_levels_distribution.py')
8. Find the best natural learner mouse. Done (find_natural_learner/)

## Technologies used:

* MySQL Workbench
* Python - mysql.connector, re

## Setup

1. Download the Data_Cortex_Nuclear.csv file from https://www.kaggle.com/ruslankl/mice-protein-expression
2. Import 'Data_Cortex_Nuclear.csv' into MySQL table using the MySQL Data Import Wizard
![Show the MySQL Data Imort Wizard](https://user-images.githubusercontent.com/47303660/75633122-348f9c80-5bfa-11ea-8701-0c26302119f3.jpg)
3. Run the 'avg_protein_levels.py' file. Inside the file the source database(your_database_1) and source table(your_table_1) has to be changed with your ones and destination database(your_database_2) and destination table(your_table_2) as well.
