# These are 3 functions that splits single protein results from single mice into 3 value ranges. 
# This method with the 3 functions works with single mouse and single protein, but when I tried to
# use it in python with multiple mice it was unable to recognize a protein name.

# This is the furst value range
DELIMITER //
CREATE FUNCTION protein_data.protein_level_type_lower()
RETURNS INT
DETERMINISTIC
BEGIN
SELECT COUNT(DYRK1A_N) FROM protein_data.protein_levels
						WHERE DYRK1A_N BETWEEN 
                        (SELECT MIN(DYRK1A_N) FROM protein_data.protein_levels WHERE MouseID REGEXP '^309_')
						AND 
						(SELECT MIN(DYRK1A_N) + ( (MAX(DYRK1A_N) - MIN(DYRK1A_N))/3 ) FROM protein_data.protein_levels 
                        WHERE MouseID REGEXP '^309_')
						AND 
MouseID REGEXP '^309_' INTO @protein_count_lower; # I got the results for the first third Wooooho		
RETURN @protein_count_lower;
END //
DELIMITER ;

SELECT protein_data.protein_level_type_lower() AS 'lower_third_count';

# This is the second value(the middle) range
DELIMITER //
CREATE FUNCTION protein_data.protein_level_type_middle()
RETURNS INT
DETERMINISTIC
BEGIN
SELECT COUNT(DYRK1A_N) FROM protein_data.protein_levels
						WHERE DYRK1A_N BETWEEN 
                        (SELECT MIN(DYRK1A_N) + ( (MAX(DYRK1A_N) - MIN(DYRK1A_N))/3 ) FROM protein_data.protein_levels 
                        WHERE MouseID REGEXP '^309_')
						AND 
						(SELECT MIN(DYRK1A_N) + ( (MAX(DYRK1A_N) - MIN(DYRK1A_N))/3 ) + ( (MAX(DYRK1A_N) - MIN(DYRK1A_N))/3 )
                        FROM protein_data.protein_levels WHERE MouseID REGEXP '^309_')
						AND
MouseID REGEXP '^309_' INTO @protein_count_middle; # I got the results for the first third Wooooho		
RETURN @protein_count_middle;
END //
DELIMITER ;

SELECT protein_data.protein_level_type_middle() AS 'middle_third_count';

# This is the 3rd value(upper) range
DELIMITER //
CREATE FUNCTION protein_data.protein_level_type_upper()
RETURNS INT
DETERMINISTIC
BEGIN
SELECT COUNT(DYRK1A_N) FROM protein_data.protein_levels
						WHERE DYRK1A_N BETWEEN 
                        (SELECT MIN(DYRK1A_N) + ( (MAX(DYRK1A_N) - MIN(DYRK1A_N))/3 ) + ( (MAX(DYRK1A_N) - MIN(DYRK1A_N))/3 )
                        FROM protein_data.protein_levels 
                        WHERE MouseID REGEXP '^309_')
						AND 
						(SELECT MAX(DYRK1A_N)
                        FROM protein_data.protein_levels WHERE MouseID REGEXP '^309_')
						AND 
MouseID REGEXP '^309_' INTO @protein_count; # I got the results for the first third Wooooho		
RETURN @protein_count;
END //
DELIMITER ;

SELECT protein_data.protein_level_type_upper() AS 'upper_third_count';

## Single mouse protein level distribution type

SELECT 'DYRK1A_N' AS 'protein', (DYRK1A_N) AS 'MIN', MAX(DYRK1A_N) AS 'MAX', (MAX(DYRK1A_N) - MIN(DYRK1A_N)) AS 'fluctuations_range',
      (SELECT protein_data.protein_level_type_lower()) AS 'lower_third_count',
      (SELECT protein_data.protein_level_type_middle()) AS 'middle_third_count',
      (SELECT protein_data.protein_level_type_upper()) AS 'upper_third_count'
FROM protein_data.protein_levels
WHERE MouseID REGEXP '^309_'; # Call all the functions and the rest of the values.

