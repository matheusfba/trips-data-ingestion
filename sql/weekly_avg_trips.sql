SELECT tmp.region, ROUND(AVG(tmp.total),2) average_weekly_trips
FROM
    (
        SELECT region, 
               DATE_PART('week', datetime) week_num, 
               COUNT(1) total
        FROM trips
        GROUP BY region, week_num
    ) AS tmp
GROUP BY tmp.region