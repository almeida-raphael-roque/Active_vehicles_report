SELECT DISTINCT
CONCAT(
    CAST(ir.id AS VARCHAR),
    CAST(irs.id AS VARCHAR),
    '1'
) AS id_conjunto,
ir.id AS matricula,
irs.id AS conjunto,
COALESCE(iv.board,it.board,itt.board) AS placa,
COALESCE(iv.chassi,it.chassi,itt.chassi) AS "chassi",
iss.description AS "status",
CAST(COALESCE(irsc.date_initial_effect,date_add('year',-1,irsc.date_final_effect)) AS DATE) AS data_ativacao,
CAST(irs.date_cancellation AS DATE) AS data_cancelamento,
'Segtruck' AS cooperativa


FROM silver.insurance_registration ir 
LEFT JOIN silver.insurance_reg_set irs ON irs.parent = ir.id
LEFT JOIN silver.insurance_reg_set_coverage irsc ON irsc.parent = irs.id
LEFT JOIN silver.insurance_reg_set_cov_trailer irsct ON irsct.parent = irsc.id
LEFT JOIN silver.insurance_status iss ON iss.id=irs.id_status
LEFT JOIN silver.insurance_vehicle iv ON iv.id=irsc.id_vehicle
LEFT JOIN silver.insurance_trailer it ON it.id=irsc.id_trailer
LEFT JOIN silver.insurance_trailer itt ON itt.id=irsct.id_trailer


WHERE COALESCE(iv.board,it.board,itt.board) IS NOT NULL
AND COALESCE(iv.chassi,it.chassi,itt.chassi) IS NOT NULL
AND CAST(irs.date_cancellation AS DATE) = date_add('day', -1, current_date)
 

--------------------------------------------------------------------------
UNION ALL
--------------------------------------------------------------------------


SELECT DISTINCT
CONCAT(
    CAST(ir.id AS VARCHAR),
    CAST(irs.id AS VARCHAR),
    '2'
) AS id_conjunto,
ir.id AS matricula,
irs.id AS conjunto,
COALESCE(iv.board,it.board,itt.board) AS placa,
COALESCE(iv.chassi,it.chassi,itt.chassi) AS "chassi",
iss.description AS "status",
CAST(COALESCE(irsc.date_initial_effect,date_add('year',-1,irsc.date_final_effect)) AS DATE) AS data_ativacao,
CAST(irs.date_cancellation AS DATE) AS data_cancelamento,
'Stcoop' AS cooperativa


FROM stcoop.insurance_registration ir 
LEFT JOIN stcoop.insurance_reg_set irs ON irs.parent = ir.id
LEFT JOIN stcoop.insurance_reg_set_coverage irsc ON irsc.parent = irs.id
LEFT JOIN stcoop.insurance_reg_set_cov_trailer irsct ON irsct.parent = irsc.id
LEFT JOIN stcoop.insurance_status iss ON iss.id=irs.id_status
LEFT JOIN stcoop.insurance_vehicle iv ON iv.id=irsc.id_vehicle
LEFT JOIN stcoop.insurance_trailer it ON it.id=irsc.id_trailer
LEFT JOIN stcoop.insurance_trailer itt ON itt.id=irsct.id_trailer


WHERE COALESCE(iv.board,it.board,itt.board) IS NOT NULL
AND COALESCE(iv.chassi,it.chassi,itt.chassi) IS NOT NULL
AND CAST(irs.date_cancellation AS DATE) = date_add('day', -1, current_date)
 

--------------------------------------------------------------------------
UNION ALL
--------------------------------------------------------------------------


SELECT DISTINCT
CONCAT(
    CAST(ir.id AS VARCHAR),
    CAST(irs.id AS VARCHAR),
    '3'
) AS id_conjunto,
ir.id AS matricula,
irs.id AS conjunto,
COALESCE(iv.board,it.board,itt.board) AS placa,
COALESCE(iv.chassi,it.chassi,itt.chassi) AS "chassi",
iss.description AS "status",
CAST(COALESCE(irsc.date_initial_effect,date_add('year',-1,irsc.date_final_effect)) AS DATE) AS data_ativacao,
CAST(irs.date_cancellation AS DATE) AS data_cancelamento,
'Viavante' AS cooperativa


FROM viavante.insurance_registration ir 
LEFT JOIN viavante.insurance_reg_set irs ON irs.parent = ir.id
LEFT JOIN viavante.insurance_reg_set_coverage irsc ON irsc.parent = irs.id
LEFT JOIN viavante.insurance_reg_set_cov_trailer irsct ON irsct.parent = irsc.id
LEFT JOIN viavante.insurance_status iss ON iss.id=irs.id_status
LEFT JOIN viavante.insurance_vehicle iv ON iv.id=irsc.id_vehicle
LEFT JOIN viavante.insurance_trailer it ON it.id=irsc.id_trailer
LEFT JOIN viavante.insurance_trailer itt ON itt.id=irsct.id_trailer


WHERE COALESCE(iv.board,it.board,itt.board) IS NOT NULL
AND COALESCE(iv.chassi,it.chassi,itt.chassi) IS NOT NULL
AND CAST(irs.date_cancellation AS DATE) = date_add('day', -1, current_date)
 