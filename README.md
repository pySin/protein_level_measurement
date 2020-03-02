# Protein Level Measurement

## Introduction
Analyse data from protein levels in the nuclear fraction of cerebral cortex in mice. The data is available at: https://www.kaggle.com/ruslankl/mice-protein-expression. The experiment uses different strategies to assess associative learning explained in the link provided. 

## Tasks

1. Compare the average levels of every protein when the mice are injected with mematine drug or not. / Done

## Technologies used:

* MySQL Workbench
* Python - mysql.connector, re

## Setup

1. Download the Data_Cortex_Nuclear.csv file from https://www.kaggle.com/ruslankl/mice-protein-expression
2. Import 'Data_Cortex_Nuclear.csv' into MySQL table using the MySQL Data Import Wizard
![Show the MySQL Data Imort Wizard](https://user-images.githubusercontent.com/47303660/75633122-348f9c80-5bfa-11ea-8701-0c26302119f3.jpg)
3. Run the 'avg_protein_levels.py' file. Inside the file the source database and source table has to be changed with your ones and destination database and destination table as well.
