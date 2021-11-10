drop table if exists graph;
CREATE TABLE graph (
	x text,
	r text,
	y text
);

INSERT INTO 
    graph (x, r, y)
VALUES
    ('1','a', '2'),
    ('1','b', '4'),
    ('2','e', '5'),
    ('2','b', '3'),
    ('2','a', '6'),
    ('3','d', '6'),
    ('3','a', '4'),
    ('4','b', '7'),
    ('5','e', '8'),
    ('6','a', '8'),
    ('6','d', '7'),
    ('7','a', '8'),
    ('8','a', '9'),
    ('8','b', '10'),
    ('9','c', '5'),
    ('10','d', '11');
    
------------------------------
--------------PLUS------------
------------------------------

WITH recursive cte(x, y) AS (
    SELECT x, y
    FROM graph g
    where r = 'a'
    UNION
    SELECT c.x, g.y 
    FROM cte c, graph g 
    WHERE c.y = g.x and g.r = 'a'
)

SELECT
x, y
FROM cte

------------------------------
-----CONCATENATION------------
------------------------------
select * from graph where r = 'a' or r ='b'

SELECT g1.x, g2.y
FROM graph g1, graph g2
WHERE g1.y = g2.x and g1.r = 'a' and g2.r = 'b'


------------------------------
-----Random Tests------------
------------------------------


WITH cte_1(x, y) AS(
SELECT g.x, g.y
FROM graph g
WHERE g.r = 'a'
)
SELECT x, y
FROM cte_1

--------------

WITH cte_2(x, y) AS(
SELECT g.x, g.y
FROM graph g
WHERE g.r = 'b'
)
SELECT x, y
FROM cte_2

--------------

WITH cte_5(x, y) AS(
SELECT l.x, r.y
FROM cte_4 l, cte_5 r
WHERE l.y = r.x 
)
SELECT x, y
FROM cte_5

--------------

WITH cte_1(x, y) AS(
SELECT g.x, g.y
FROM graph g
WHERE g.r = 'a'
),

cte_2(x, y) AS(
SELECT g.x, g.y
FROM graph g
WHERE g.r = 'b'
),

cte_3(x, y) AS(
SELECT l.x, r.y
FROM cte_1 l, cte_2 r
WHERE l.y = r.x 
)
SELECT x, y
FROM cte_3


--------------

WITH recursive cte_1(x, y) AS(
SELECT g.x, g.y
FROM graph g
WHERE g.r = 'a'
),

cte_2(x, y) AS(
SELECT g.x, g.y
FROM graph g
WHERE g.r = 'b'
),

cte_3(x, y) AS(
SELECT l.x, r.y
FROM cte_1 l, cte_2 r
WHERE l.y = r.x 
),

cte_4(x, y) AS(
SELECT x, y
FROM cte_3 g
UNION
SELECT c.x, g.y
FROM cte_4 c, cte_3 g
WHERE c.y = g.x
)

SELECT x, y
FROM cte_4

--------------

WITH recursive cte_1(x, y) AS(
SELECT g.x, g.y
FROM graph g
WHERE g.r = 'a'
),

cte_2(x, y) AS(
SELECT g.x, g.y
FROM graph g
WHERE g.r = 'b'
),

cte_3(x, y) AS(
SELECT l.x, r.y
FROM cte_1 l, cte_2 r
WHERE l.y = r.x 
),

cte_4(x, y) AS(
SELECT x, y
FROM cte_3 g
UNION
SELECT c.x, g.y
FROM cte_4 c, cte_3 g
WHERE c.y = g.x
),

cte_5(x, y) AS(
SELECT g.x, g.y
FROM graph g
WHERE g.r = 'd'
),

cte_6(x, y) AS(
SELECT l.x, r.y
FROM cte_4 l, cte_5 r
WHERE l.y = r.x 
)
SELECT x, y
FROM cte_6

--------------












