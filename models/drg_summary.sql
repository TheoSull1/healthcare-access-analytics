-- DRG summary
SELECT drg_cd, 
	drg_desc, 
	nat_tot_dschrgs, 
	ROUND(nat_avg_submtd_chrg - nat_avg_mdcr_pymt,2) AS nat_gap_dollars,
	ROUND(nat_avg_submtd_chrg/nat_avg_mdcr_pymt,2) AS nat_gap_ratio
FROM (
	SELECT drg_cd,
		drg_desc,
		sum(tot_dschrgs) AS nat_tot_dschrgs,
		SUM(avg_submtd_chrg * tot_dschrgs) / SUM(tot_dschrgs) AS nat_avg_submtd_chrg,
		SUM(avg_mdcr_pymt * tot_dschrgs) / SUM(tot_dschrgs) AS nat_avg_mdcr_pymt
	FROM inpatient_claims
	GROUP BY drg_cd, drg_desc
	) base
ORDER BY ROUND(nat_avg_submtd_chrg - nat_avg_mdcr_pymt,2) DESC