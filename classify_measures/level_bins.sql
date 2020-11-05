# Transform a measure protein column into a class then use this class ranges to check if the other proteins synchronize with
# those ranges in any way.

# The source table is 'protein_info.protein_levels'
# Create 2 copies of the main 'Protein Levels' table.alter

CREATE TABLE protein_info.protein_levels_b AS
SELECT * FROM protein_info.protein_levels;

CREATE TABLE protein_info.protein_levels_c AS
SELECT * FROM protein_info.protein_levels;

# Change the values of the first protein 'DYRK1A_N' to 4 ranges(bins). The protein's variation range is devided to 4 ranges. The full 
# variation range is the MAX value minus the MIN value. All protein levels are in this range. So MIN(protein) + 25% of the range is the first
# subrange. The 4 subranges are 0% - 25%, 25% - 50%, 50% - 75% and 75% - 100%. The labels we will use for this bins are 1, 2, 3, 4 for simplicity.

UPDATE protein_info.protein_levels_b 
SET DYRK1A_N = (CASE
					WHEN DYRK1A_N BETWEEN (SELECT MIN(DYRK1A_N) FROM protein_info.protein_levels_c) 
                    AND (SELECT MIN(DYRK1A_N) + ((MAX(DYRK1A_N) - MIN(DYRK1A_N))/4) FROM protein_info.protein_levels_c)
                    THEN 1
                    WHEN DYRK1A_N BETWEEN (SELECT MIN(DYRK1A_N) + ((MAX(DYRK1A_N) - MIN(DYRK1A_N))/4) FROM protein_info.protein_levels_c)
                    AND (SELECT MIN(DYRK1A_N) + (((MAX(DYRK1A_N) - MIN(DYRK1A_N))/4)*2) FROM protein_info.protein_levels_c)
                    THEN 2
					WHEN DYRK1A_N BETWEEN (SELECT MIN(DYRK1A_N) + (((MAX(DYRK1A_N) - MIN(DYRK1A_N))/4)*2) FROM protein_info.protein_levels_c)
                    AND (SELECT MIN(DYRK1A_N) + (((MAX(DYRK1A_N) - MIN(DYRK1A_N))/4)*3) FROM protein_info.protein_levels_c)
                    THEN 3
					WHEN DYRK1A_N BETWEEN (SELECT MIN(DYRK1A_N) + (((MAX(DYRK1A_N) - MIN(DYRK1A_N))/4)*3) FROM protein_info.protein_levels_c)
                    AND(SELECT MIN(DYRK1A_N) + (((MAX(DYRK1A_N) - MIN(DYRK1A_N))/4)*4) FROM protein_info.protein_levels_c)
                    THEN 4
					END);
                    
# Check if the changes has been made.
SELECT * FROM protein_info.protein_levels_b;

# Take the next 5 columns(5 proteins) and give their average for every subrange of the main protein(DYRK1A_N). Make a new table for it.

CREATE TABLE protein_info.level_bins AS
SELECT DYRK1A_N, AVG(ITSN1_N) AS 'AVG_ITSN1_N', AVG(BDNF_N) AS 'AVG_BDNF_N', AVG(NR1_N) AS 'AVG_NR1_N', AVG(NR2A_N) AS 'AVG_NR2A_N',
	   AVG(pAKT_N) AS 'AVG_pAKT_N'
FROM protein_info.protein_levels_b
GROUP BY DYRK1A_N
ORDER BY DYRK1A_N ASC;

SELECT * FROM protein_info.level_bins;

# Check if the subranges from the main protein(DYRK1A_N) shows similarities with another protein(ITSN1_N). 
# The second protein can be any of the other proteins.

SELECT 'DYRK1A_N - ITSN1_N' AS 'P-COR', (CASE
WHEN
(SELECT AVG_ITSN1_N FROM protein_info.level_bins WHERE DYRK1A_N = 1) < (SELECT AVG_ITSN1_N FROM protein_info.level_bins WHERE DYRK1A_N = 2)
< (SELECT AVG_ITSN1_N FROM protein_info.level_bins WHERE DYRK1A_N = 3) < (SELECT AVG_ITSN1_N FROM protein_info.level_bins WHERE DYRK1A_N = 4)
THEN 'Yes'
ELSE 'No' 
END) AS 'Similarity';
