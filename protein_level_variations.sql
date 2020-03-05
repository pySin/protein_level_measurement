## Protein Variation Range

# Compare the expression variations of single protein in single mouse. The 'percent_difference'
# column shows the range of variability in percentages.

CREATE TABLE protein_data.protein_exp_variations AS
WITH normal_non_stimulated AS
(SELECT * FROM protein_data.protein_levels
WHERE class = 'c-SC-s'
UNION ALL
SELECT * FROM protein_data.protein_levels 
WHERE class = 'c-SC-m') 
(SELECT SUBSTRING(MouseID, 1, 4) AS 'mouse_id', Treatment, 'SYP_N' AS 'Protein', MIN(SYP_N) AS 'MIN', MAX(SYP_N) AS 'MAX', ROUND(100-((MIN(SYP_N)/MAX(SYP_N))*100)) AS 'percent_difference'
FROM normal_non_stimulated
GROUP BY SUBSTRING(MouseID, 1, 4))
UNION ALL
(SELECT SUBSTRING(MouseID, 1, 4) AS 'mouse_id', Treatment, 'EGR1_N', MIN(EGR1_N), MAX(EGR1_N), ROUND(100-((MIN(EGR1_N)/MAX(EGR1_N))*100)) AS 'percent_difference'
FROM normal_non_stimulated
GROUP BY SUBSTRING(MouseID, 1, 4))
UNION ALL
(SELECT SUBSTRING(MouseID, 1, 4) AS 'mouse_id', Treatment, 'H3MeK4_N', MIN(H3MeK4_N), MAX(H3MeK4_N), ROUND(100-((MIN(H3MeK4_N)/MAX(H3MeK4_N))*100)) AS 'percent_difference'
FROM normal_non_stimulated
GROUP BY SUBSTRING(MouseID, 1, 4))
UNION ALL
(SELECT SUBSTRING(MouseID, 1, 4) AS 'mouse_id', Treatment, 'CaNA_N', MIN(CaNA_N), MAX(CaNA_N), ROUND(100-((MIN(CaNA_N)/MAX(CaNA_N))*100)) AS 'percent_difference'
FROM normal_non_stimulated
GROUP BY SUBSTRING(MouseID, 1, 4));

# Check the new table
SELECT * FROM protein_data.protein_exp_variations;