--1.
SELECT COUNT(*)
FROM film f
INNER JOIN (
    SELECT film_id, COUNT(*)
    FROM film_actor
    GROUP BY film_id
    HAVING COUNT(*) > 15
    ) AS film2
ON f.film_id = film2.film_id;

--2.
--It doesn't match the value from VARIANCE(amount) but I don't know why
SELECT SUM(payment2.number)/(COUNT(*)-1)
FROM payment
INNER JOIN (
    SELECT customer_id, POWER((amount-(
        SELECT AVG(amount)
        FROM payment
        )),2) AS number
    FROM payment
) AS payment2 on payment.customer_id = payment2.customer_id;

--3.
SELECT *
FROM rental
WHERE staff_id = 2 AND rental_id = (
    SELECT film_id
    FROM film
    WHERE title = 'HIGHBALL POTTER'
    );
