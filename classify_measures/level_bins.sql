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

# Take all the proteins and give their average for every subrange of the main protein(DYRK1A_N). Make a new table for it.

CREATE TABLE protein_info.level_bins AS
SELECT DYRK1A_N, 
	AVG(ITSN1_N) AS 'AVG_ITSN1_N', 
	AVG(BDNF_N) AS 'AVG_BDNF_N', 
    AVG(NR1_N) AS 'AVG_NR1_N', 
    AVG(NR2A_N) AS 'AVG_NR2A_N', 
    AVG(pAKT_N) AS 'AVG_pAKT_N', 
    AVG(pBRAF_N) AS 'AVG_pBRAF_N', 
    AVG(pCAMKII_N) AS 'AVG_pCAMKII_N', 
    AVG(pCREB_N) AS 'AVG_pCREB_N', 
    AVG(pELK_N) AS 'AVG_pELK_N', 
    AVG(pERK_N) AS 'AVG_pERK_N', 
    AVG(pJNK_N) AS 'AVG_pJNK_N', 
    AVG(PKCA_N) AS 'AVG_PKCA_N', 
    AVG(pMEK_N) AS 'AVG_pMEK_N', 
    AVG(pNR1_N) AS 'AVG_pNR1_N',
    AVG(pNR2A_N) AS 'AVG_pNR2A_N', 
    AVG(pNR2B_N) AS 'AVG_pNR2B_N',
    AVG(pPKCAB_N) AS 'AVG_pPKCAB_N',
    AVG(pRSK_N) AS 'AVG_pRSK_N', 
    AVG(AKT_N) AS 'AVG_AKT_N',
    AVG(BRAF_N) AS 'AVG_BRAF_N',
    AVG(CAMKII_N) AS 'AVG_CAMKII_N',
    AVG(CREB_N) AS 'AVG_CREB_N', 
    AVG(ELK_N) AS 'AVG_ELK_N',
    AVG(ERK_N) AS 'AVG_ERK_N',
    AVG(GSK3B_N) AS 'AVG_GSK3B_N', 
    AVG(JNK_N) AS 'AVG_JNK_N', 
    AVG(MEK_N) AS 'AVG_MEK_N', 
    AVG(TRKA_N) AS 'AVG_TRKA_N', 
    AVG(RSK_N) AS 'AVG_RSK_N', 
    AVG(APP_N) AS 'AVG_APP_N', 
    AVG(Bcatenin_N) AS 'AVG_Bcatenin_N',
    AVG(SOD1_N) AS 'AVG_SOD1_N',
    AVG(MTOR_N) AS 'AVG_MTOR_N',
    AVG(P38_N) AS 'AVG_P38_N', 
    AVG(pMTOR_N) AS 'AVG_pMTOR_N',
    AVG(DSCR1_N) AS 'AVG_DSCR1_N',
    AVG(AMPKA_N) AS 'AVG_AMPKA_N',
    AVG(NR2B_N) AS 'AVG_NR2B_N', 
    AVG(pNUMB_N) AS 'AVG_pNUMB_N', 
    AVG(RAPTOR_N) AS 'AVG_RAPTOR_N', 
    AVG(TIAM1_N) AS 'AVG_TIAM1_N', 
    AVG(pP70S6_N) AS 'AVG_pP70S6_N', 
    AVG(NUMB_N) AS 'AVG_NUMB_N', 
    AVG(P70S6_N) AS 'AVG_P70S6_N', 
    AVG(pGSK3B_N) AS 'AVG_pGSK3B_N', 
    AVG(pPKCG_N) AS 'AVG_pPKCG_N',
    AVG(CDK5_N) AS 'AVG_CDK5_N', 
    AVG(S6_N) AS 'AVG_S6_N', 
    AVG(ADARB1_N) AS 'AVG_ADARB1_N', 
    AVG(AcetylH3K9_N) AS 'AVG_AcetylH3K9_N',
    AVG(RRP1_N) AS 'AVG_RRP1_N',
    AVG(BAX_N) AS 'AVG_BAX_N', 
    AVG(ARC_N) AS 'AVG_ARC_N', 
    AVG(ERBB4_N) AS 'AVG_ERBB4_N', 
    AVG(nNOS_N) AS 'AVG_nNOS_N', 
    AVG(Tau_N) AS 'AVG_Tau_N', 
    AVG(GFAP_N) AS 'AVG_GFAP_N', 
    AVG(GluR3_N) AS 'AVG_GluR3_N', 
    AVG(GluR4_N) AS 'AVG_GluR4_N', 
    AVG(IL1B_N) AS 'AVG_IL1B_N', 
    AVG(P3525_N) AS 'AVG_P3525_N',
    AVG(pCASP9_N) AS 'AVG_pCASP9_N',
    AVG(PSD95_N) AS 'AVG_PSD95_N',
    AVG(SNCA_N) AS 'AVG_SNCA_N', 
    AVG(Ubiquitin_N) AS 'AVG_Ubiquitin_N',
    AVG(pGSK3B_Tyr216_N) AS 'AVG_pGSK3B_Tyr216_N',
    AVG(SHH_N) AS 'AVG_SHH_N', 
    AVG(BAD_N) AS 'AVG_BAD_N',
    #AVG(BCL2_N) AS 'AVG_BCL2_N', # didn't accept this column for some reason?!
    AVG(pS6_N) AS 'AVG_pS6_N',
    AVG(pCFOS_N) AS 'AVG_pCFOS_N',
    AVG(SYP_N) AS 'AVG_SYP_N', 
    AVG(H3AcK18_N) AS 'AVG_H3AcK18_N', 
    AVG(EGR1_N) AS 'AVG_EGR1_N',
    AVG(H3MeK4_N) AS 'AVG_H3MeK4_N', 
    AVG(CaNA_N) AS 'AVG_CaNA_N'
FROM protein_info.protein_levels_b
GROUP BY DYRK1A_N
ORDER BY DYRK1A_N ASC;
