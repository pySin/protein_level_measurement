# Create new table for the average concentration values for a protein when 
# Memantin drug is used and when it's not used. Does Memantine influence
# the level of expression of the protein in focus.
CREATE TABLE protein_data.avg_p_concentration(
protein VARCHAR(30),
avg_memantine FLOAT,
avg_saline FLOAT
);

## Populate tha tables with the average values 
INSERT INTO protein_data.avg_p_concentration(protein, avg_memantine, avg_saline)
VALUES('DYRK1A_N',

(SELECT AVG(DYRK1A_N) FROM protein_data.protein_levels
WHERE Treatment = 'Memantine'),

(SELECT AVG(DYRK1A_N) FROM protein_data.protein_levels
WHERE Treatment = 'Saline')
);

# Check if data is inserted properly
SELECT * FROM protein_data.avg_p_concentration;