SELECT region,
       datasource,
       count(1) quantity
FROM trips
WHERE datasource = 'cheap_mobile'
GROUP BY region,
         datasource
ORDER BY quantity DESC