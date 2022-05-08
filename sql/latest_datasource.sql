SELECT region,
       datasource,
       datetime
FROM
  (SELECT region,
          datasource,
          datetime,
          ROW_NUMBER() OVER(PARTITION BY region
                            ORDER BY datetime DESC) row_num
   FROM trips
   WHERE region IN
       (SELECT region
        FROM
          (SELECT region,
                  COUNT(1) total
           FROM trips
           GROUP BY region
           ORDER BY total DESC
           LIMIT 2) tmp1)) tmp2
WHERE row_num = 1