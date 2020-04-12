# Find natural learner mouse among normal mice.

# Create 5 more columns calculating the difference between the average protein levels for all stimulated mice for every protein
# and the average protein levels for every normal mouse. Thus we can find the difference between an average stimulated mouse 
# and every normal mouse. 

CREATE TABLE protein_data.s_protein_difference AS
SELECT *, 
ABS(FORMAT(AVG_stimulated - normal_mouse_3422, 6)) AS 'Difference_3422',
ABS(FORMAT(AVG_stimulated - normal_mouse_3423, 6)) AS 'Difference_3423',
ABS(FORMAT(AVG_stimulated - normal_mouse_3488, 6)) AS 'Difference_3488',
ABS(FORMAT(AVG_stimulated - normal_mouse_3489, 6)) AS 'Difference_3489',
ABS(FORMAT(AVG_stimulated - normal_mouse_3490, 6)) AS 'Difference_3490'
FROM protein_data.find_natural_learner;

# Check on the newly created table.
SELECT * FROM protein_data.s_protein_difference;

# Create table showing the difference between the SUM of averages for all prooteins when mice are stimulated
# and the SUM of the average levels of all proteins for 1 normal mouse. In this way the protein level profile
# for the average stimulated mice is compared with the protein profile for evry normal mouse. The normal mice
# profile which is the closest to the avevarage stimulated profile might me considered 'the best natural learner'.
# If a normal mouse expresses protein levels of stimulated mouse without stimulation it could be considered as
# naturally stimulated to learn. 

CREATE TABLE protein_data.natural_learner_results AS
SELECT 'stimulated_to_learn_mouse' AS 'difference_from', 
FORMAT(SUM(Difference_3422), 6) AS 'normal_mouse_3422', FORMAT(SUM(Difference_3423), 6) AS 'normal_mouse_3423',
FORMAT(SUM(Difference_3488), 6) AS 'normal_mouse_3488', FORMAT(SUM(Difference_3489), 6) AS 'normal_mouse_3489', 
FORMAT(SUM(Difference_3490), 6) AS 'normal_mouse_3490'
FROM protein_data.s_protein_difference;

# Check the new table
SELECT * FROM protein_data.natural_learner_results;

# Create a temporary table to transfer the results from different columns into 1 column
CREATE TEMPORARY TABLE protein_data.temp_close_p AS
SELECT 'normal_mouse_3422' AS 'normal_mouse', normal_mouse_3422 AS 'similarity_compare' FROM protein_data.natural_learner_results
UNION
SELECT 'normal_mouse_3423', normal_mouse_3423 FROM protein_data.natural_learner_results
UNION
SELECT 'normal_mouse_3488', normal_mouse_3488 FROM protein_data.natural_learner_results
UNION
SELECT 'normal_mouse_3489', normal_mouse_3489 FROM protein_data.natural_learner_results
UNION
SELECT 'normal_mouse_3490', normal_mouse_3490 FROM protein_data.natural_learner_results; 

# Check the new table
SELECT * FROM protein_data.temp_close_p;

# Select the lowest result from the temporary table. This is the mouse that shows the smallest difference from 
# a stimulated to learn mouse. This is our mouse natural learner.
CREATE TABLE protein_data.natural_learner_winner
SELECT normal_mouse, similarity_compare   
FROM protein_data.temp_close_p
ORDER BY ABS(similarity_compare) ASC
LIMIT 1;
