USE sakila;

-- 1a. Display the first and last names of all actors from the table actor.
SELECT first_name, last_name 
FROM actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
SELECT CONCAT(first_name, ' ', last_name) AS Actor_Name 
FROM actor;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." 
SELECT actor_id, first_name, last_name 
FROM actor 
WHERE first_name="Joe";

-- 2b. Find all actors whose last name contain the letters GEN:
SELECT * FROM actor 
WHERE last_name 
LIKE '%GEN%';

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
SELECT * FROM actor 
WHERE last_name 
LIKE '%Li%'  
ORDER BY last_name, first_name;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT country_id, country 
FROM country 
WHERE country IN ("Afghanistan", "Bangladesh", "China");

-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).
ALTER TABLE actor 
ADD COLUMN description BLOB;

DESCRIBE actor;

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
ALTER TABLE actor 
DROP COLUMN description;

-- 4a. List the last names of actors, as well as how many actors have that last name.
SELECT last_name, COUNT(last_name) 
FROM actor 
GROUP BY last_name;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
SELECT last_name, COUNT(last_name) 
FROM actor 
GROUP BY last_name
HAVING COUNT(last_name)>1;

-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.
UPDATE actor SET first_name = "HARPO" 
WHERE first_name ="GROUCHO" AND last_name = "WILLIAMS";

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
UPDATE actor SET first_name = "GROUCHO" 
WHERE first_name ="HARPO" AND last_name = "WILLIAMS";

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
SHOW CREATE TABLE address;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
SELECT first_name, last_name, address.address
FROM staff
JOIN address 
		using (address_id);

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
SELECT staff.staff_id, first_name, last_name, SUM(payment.amount)
FROM staff
RIGHT JOIN payment  
		using (staff_id)
WHERE payment_date LIKE '2005-08%'
GROUP BY staff_id;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
SELECT film.film_id, title, COUNT(actor_id)
FROM film_actor
INNER JOIN film  
		using (film_id)
GROUP BY film_id;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT COUNT(inventory_id)
AS 'Num of Copies "Hunchback Impossible"'
FROM inventory
WHERE inventory.film_id = (
			SELECT film_id 
			FROM film
			WHERE title = "Hunchback Impossible")
GROUP BY inventory.film_id;

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
SELECT customer.customer_id, first_name, last_name, SUM(amount)
FROM payment
LEFT JOIN customer 
		using (customer_id)
GROUP BY customer_id
ORDER BY last_name, first_name;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
SELECT title, film.language_id
FROM film 
WHERE title LIKE 'K%' OR title LIKE 'Q%' 
AND film.language_id = (
			SELECT language.language_id
			FROM language
			WHERE name = "English");

-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
SELECT actor.actor_id, first_name, last_name, film_id
FROM actor
INNER JOIN film_actor
		using (actor_id)
WHERE film_id = (
			SELECT film.film_id
			FROM film
			WHERE title = "Alone Trip");

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
SELECT first_name, last_name, address.city_id
FROM customer
INNER JOIN address
		using (address_id)
WHERE city_id IN (	#Get customers from selection of cities
			SELECT city.city_id #Get list cities in Canada
			FROM city
			WHERE city.country_id =(
							SELECT country.country_id # Get id of Canada
							FROM country
							WHERE country = "Canada"));

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
SELECT title
FROM film
WHERE film.film_id IN (
			SELECT film_category.film_id
			FROM film_category
			WHERE category_id = (
						SELECT category.category_id
						FROM category
						WHERE category.name = "Family"));

-- 7e. Display the most frequently rented movies in descending order.
SELECT i.film_id, rental_date, title
FROM inventory i
INNER JOIN rental r
		on i.inventory_id = r.inventory_id
INNER JOIN film f
		on f.film_id = i.film_id
ORDER BY rental_date DESC limit 10;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
SELECT store.store_id, SUM(amount)
FROM staff
INNER JOIN payment p
		on staff.staff_id = p.staff_id
INNER JOIN store
		on store.store_id = staff.store_id
GROUP BY store_id;

-- 7g. Write a query to display for each store its store ID, city, and country.
SELECT DISTINCT s.store_id, address, city, country
FROM store s
INNER JOIN address a
		on a.address_id = s.address_id
INNER JOIN city c
		on c.city_id = a.city_id
INNER JOIN country
		on country.country_id = c.country_id;

-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
SELECT DISTINCT c.name, SUM(p.amount)
FROM category c
INNER JOIN film_category fc
		on c.category_id = fc.category_id
INNER JOIN inventory i
		on fc.film_id = i.film_id
INNER JOIN rental r
		on i.inventory_id = r.inventory_id
INNER JOIN payment p
		on p.rental_id = r.rental_id
GROUP BY c.name
ORDER BY SUM(p.amount) DESC limit 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
CREATE VIEW Top_5_genres AS

SELECT DISTINCT c.name, SUM(p.amount)
FROM category c
INNER JOIN film_category fc
		on c.category_id = fc.category_id
INNER JOIN inventory i
		on fc.film_id = i.film_id
INNER JOIN rental r
		on i.inventory_id = r.inventory_id
INNER JOIN payment p
		on p.rental_id = r.rental_id
GROUP BY c.name
ORDER BY SUM(p.amount) DESC limit 5;

-- 8b. How would you display the view that you created in 8a?
SELECT * FROM Top_5_genres;

-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
DROP VIEW Top_5_genres;



