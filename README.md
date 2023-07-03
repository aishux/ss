WITH COMMON_COST_CENTER AS (
    SELECT A.COST_CENTER_CODE
    FROM governed.gmis_hierarchy_cema_cost_center_governed A
    JOIN governed.input_table B ON A.COST_CENTER_CODE = B.EXT_CC_IDENT
    WHERE A.AS_OF_DT = '202012311'
),
PARENT_CODE_FOUND AS (
    SELECT DISTINCT A.PARENT_COST_CENTER_CODE, A.COST_CENTER_CODE
    FROM governed.gmis_hierarchy_cema_cost_center_governed A
    WHERE A.PARENT_COST_CENTER_CODE IN (
        SELECT COST_CENTER_CODE
        FROM COMMON_COST_CENTER
    ) AND A.AS_OF_DT = '20201231'
),
PARENT_CODE_NOT_FOUND AS (
    SELECT A.COST_CENTER_CODE, NULL AS REP_CC
    FROM governed.gmis_hierarchy_cema_cost_center_governed A
    WHERE A.COST_CENTER_CODE IN (
        SELECT COST_CENTER_CODE
        FROM COMMON_COST_CENTER
    ) AND A.COST_CENTER_CODE NOT IN (
        SELECT PARENT_COST_CENTER_CODE
        FROM PARENT_CODE_FOUND
    ) AND A.AS_OF_DT = '20201231'
),
REP_CC_FIND AS (
    SELECT A.COST_CENTER_CODE, A.REP_CC
    FROM governed.gmis_hierarchy_cema_cost_center_governed A
    WHERE A.COST_CENTER_CODE IN (
        SELECT PARENT_COST_CENTER_CODE
        FROM PARENT_CODE_FOUND
    ) AND A.AS_OF_DT = '20201231' AND A.REP_CC IS NOT NULL
),
REP_CC_NULL_FIND AS (
    SELECT A.COST_CENTER_CODE, A.REP_CC
    FROM governed.gmis_hierarchy_cema_cost_center_governed A
    WHERE A.COST_CENTER_CODE IN (
        SELECT PARENT_COST_CENTER_CODE
        FROM PARENT_CODE_FOUND
    ) AND A.AS_OF_DT = '120201231'
),
REP_CC_NULL AS (
    SELECT A.COST_CENTER_CODE, A.PARENT_COST_CENTER_CODE
    FROM governed.gmis_hierarchy_cema_cost_center_governed A
    WHERE A.COST_CENTER_CODE IN (
        SELECT PARENT_COST_CENTER_CODE
        FROM PARENT_CODE_FOUND
    ) AND A.AS_OF_DT = '20201231' AND A.REP_CC IS NULL
),
REP_CC_ALL AS (
    SELECT COST_CENTER_CODE, REP_CC
    FROM REP_CC_FIND
    UNION
    SELECT COST_CENTER_CODE, REP_CC
    FROM REP_CC_NULL_FIND
    UNION
    SELECT COST_CENTER_CODE, NULL AS REP_CC
    FROM PARENT_CODE_NOT_FOUND
)
SELECT COST_CENTER_CODE, REP_CC
FROM REP_CC_ALL
