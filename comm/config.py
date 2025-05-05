CONFIG = {
    "GF": {
        "table_name": "PROVISION.CC_COMMENTARY_CUBE2_VW",
        "columns": [
            "ACCOUNT_ID", "ACCOUNT_DESC", "FUNCTION_ID", "FUNCTION_DESC",
            "REPORT_ID", "PERIOD", "REPORTING_DATE", "REPORTING_VIEW", 
            "LEAF_FUNC_DESC", "COMMENT", "CREATED_BY", "CREATED_ON", "BUSINESS_DIVISION"
        ],
        "output_table": "etl.frs_gf"
    },
    "IB": {
        "table_name": "PROVISION.CC_COMMENTARY_CUBE2_VW",
        "columns": [
            "ACCOUNT_ID", "ACCOUNT_DESC", "FUNCTION_ID", "FUNCTION_DESC",
            "REPORT_ID", "PERIOD", "REPORTING_DATE", "REPORTING_VIEW", 
            "LEAF_FUNC_DESC", "COMMENT", "CREATED_BY", "CREATED_ON", "BUSINESS_DIVISION"
        ],
        "output_table": "etl.frs_ib"
    },
    "GWM": {
        "table_name": "PROVISION.CC_COMMENTARY_CUBE2_VW",
        "columns": [
            "ACCOUNT_ID", "ACCOUNT_DESC", "FUNCTION_ID", "FUNCTION_DESC",
            "REPORT_ID", "PERIOD", "REPORTING_DATE", "REPORTING_VIEW", 
            "LEAF_FUNC_DESC", "COMMENT", "CREATED_BY", "CREATED_ON", "BUSINESS_DIVISION"
        ],
        "output_table": "etl.frs_gwm"
    },
    "DEFAULT": {
        "table_name": "PROVISION.CC_COMMENTARY_CUBE2_VW",
        "columns": [
            "ACCOUNT_ID", "ACCOUNT_DESC", "FUNCTION_ID", "FUNCTION_DESC",
            "REPORT_ID", "PERIOD", "REPORTING_DATE", "REPORTING_VIEW", 
            "LEAF_FUNC_DESC", "COMMENT", "CREATED_BY", "CREATED_ON", "BUSINESS_DIVISION"
        ],
        "output_table": "etl.frs_default"
    }
}
