check_type_sql_mappings = {
    'row_count': "SELECT sum(counts) FROM (SELECT {}, count(*) as counts FROM {} GROUP BY {}) t",
    'duplicate_count': "WITH frequencies AS ( SELECT {}, COUNT(*) AS frequency FROM {} "
                       "WHERE {} IS NOT NULL GROUP BY {} ) "
                       "SELECT COALESCE(SUM({}),0) AS duplicate_count "
                       "FROM frequencies WHERE frequency > 1 LIMIT 100",
    'duplicate_percent': "WITH frequencies AS ( SELECT {}, COUNT(*) AS frequency FROM {} WHERE {} IS NOT NULL "
                         "GROUP BY {} ), "
                         "total_count AS ( SELECT sum(frequency) AS total_count FROM frequencies), "
                         "duplicate_count AS ( SELECT count({}) AS duplicate_count "
                         "FROM frequencies WHERE frequency > 1) SELECT "
                         "COALESCE(duplicate_count * 1.0 / total_count, 0.0)*100 AS duplicate_percentage "
                         "FROM total_count, duplicate_count",
    'avg_length': "SELECT COALESCE(sum(total_length)*1.0/sum(counts), 0.0) FROM "
                  "(SELECT LENGTH({})*counts total_length, counts FROM "
                  "(SELECT {}, count(*) counts FROM {} WHERE {} IS NOT NULL GROUP BY {}) t) t1",
    'max_length': "SELECT MAX(LENGTH({})) FROM (SELECT {} FROM {}) t",
    'min_length': "SELECT MIN(LENGTH({})) FROM (SELECT {} FROM {}) t",
    'max': "SELECT MAX({}) FROM (SELECT {} FROM {}) t",
    'min': "SELECT MIN({}) FROM (SELECT {} FROM {}) t",
    'sum': "SELECT SUM({}*counts) FROM (SELECT {}, count(*) as counts FROM {} WHERE {} IS NOT NULL GROUP BY {}) t",
    'avg': "SELECT SUM({}*counts)/SUM(counts) FROM (SELECT {}, count(*) as counts "
           "FROM {} WHERE {} IS NOT NULL GROUP BY {}) t",

    'missing_count': 'SELECT counts FROM ( SELECT {}, count(*) as counts FROM {} group by {} ) t where {} IS NULL',
    'missing_percent': 'SELECT COALESCE( SUM(CASE WHEN {} IS NULL THEN counts ELSE 0 END) '
                       '/ NULLIF(SUM(counts), 0), 0 ) FROM '
                       '( SELECT {}, count(*) as counts FROM {} GROUP BY {} ) t',
    'invalid_count': {
        'invalid values': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND ({} IN ({})) THEN counts END), 0) "
                          "FROM (SELECT {}, count(*) as counts FROM {} group by 1) t",
        'valid values': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT ({} IN ({})) THEN counts END), 0) "
                        "FROM (SELECT {}, count(*) as counts FROM {} group by 1) t",
        'valid length': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT (LENGTH({}) = {}) THEN counts END),0) "
                        "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
        'valid max length': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT (LENGTH({}) <= {}) "
                            "THEN counts END),0) "
                            "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
        'valid min length': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT (LENGTH({}) >= {}) "
                            "THEN counts END),0) "
                            "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
        'valid min': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT ({} >= {}) THEN counts END),0) "
                     "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
        'valid max': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT ({} <= {}) THEN counts END),0) "
                     "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
    },
    'invalid_percent': {
        'invalid values': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND ({} IN ({})) THEN counts END)*1.0, 0)"
                          "/SUM(counts)*100 "
                          "FROM (SELECT {}, count(*) as counts FROM {} group by 1) t",
        'valid values': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT ({} IN ({})) THEN counts END)*1.0, 0) "
                        "/SUM(counts)*100 "
                        "FROM (SELECT {}, count(*) as counts FROM {} group by 1) t",
        'valid length': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT (LENGTH({}) = {}) THEN counts END)"
                        "*1.0, 0)/SUM(counts)*100 "
                        "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
        'valid max length': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT (LENGTH({}) <= {}) "
                            "THEN counts END)*1.0, 0)/SUM(counts)*100 "
                            "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
        'valid min length': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT (LENGTH({}) >= {}) "
                            "THEN counts END)*1.0, 0)/SUM(counts)*100 "
                            "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
        'valid min': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT ({} >= {}) "
                     "THEN counts END)*1.0, 0)/SUM(counts)*100 "
                     "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
        'valid max': "SELECT COALESCE(SUM(CASE WHEN NOT ({} IS NULL) AND NOT ({} <= {}) "
                     "THEN counts END)*1.0, 0)/SUM(counts)*100 "
                     "FROM (SELECT {}, count(*) as counts from {} GROUP BY 1) t",
    },
    'freshness': "SELECT (CAST(ROUND(EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)) AS INT) - "
                 "CAST(ROUND(EXTRACT(EPOCH FROM MAX({}))) AS INT) ) / 86400 "
                 "FROM (SELECT {} from {}) t",
}
