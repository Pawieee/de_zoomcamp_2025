# Week 1 Solutions

1. Run the following command to fetch the container if it doesn't exist yet and build the image:
    ```bash
    docker run -it python:3.12.8 bash
    ```
    Next, run `pip --version` and the version will be printed in the terminal.

2. Since we're using a docker-compose file, we'll use the service name as the hostname when connecting to the database using pgAdmin. The port mapping looks like this: `XXXX:YYYY`, where `XXXX` represents the host network and `YYYY` represents the container network. To connect, we'll use `YYYY`. The final answer is:
    ```
    db:5432
    ```

3. SQL Queries and Results:
    ```sql
    SELECT COUNT(*) 
    FROM public.green_taxi
    WHERE trip_distance > 1;
    -- Result: 104,838

    SELECT COUNT(*) 
    FROM public.green_taxi
    WHERE trip_distance > 1 AND trip_distance <= 3;
    -- Result: 199,013

    SELECT COUNT(*) 
    FROM public.green_taxi
    WHERE trip_distance > 3 AND trip_distance <= 7;
    -- Result: 109,645

    SELECT COUNT(*) 
    FROM public.green_taxi
    WHERE trip_distance > 7 AND trip_distance <= 10;
    -- Result: 27,688

    SELECT COUNT(*) 
    FROM public.green_taxi
    WHERE trip_distance > 10;
    -- Result: 35,202
    ```

4. SQL Query and Result:
    ```sql
    SELECT lpep_pickup_datetime::DATE AS length_Day
    FROM public.green_taxi
    WHERE trip_distance = (SELECT MAX(trip_distance) FROM public.green_taxi);
    -- Result: 2019-10-31
    ```

5. SQL Query and Results:
    ```sql
    WITH locs AS (
         SELECT "PULocationID" AS pickup_id
         FROM public.green_taxi
         WHERE lpep_pickup_datetime::DATE = '2019-10-18'
         GROUP BY "PULocationID"
         HAVING SUM(total_amount) > 13000
         ORDER BY SUM(total_amount) DESC
    )
    SELECT CONCAT("Borough", ', ', "Zone") AS area
    FROM public.taxi_zone t 
    INNER JOIN locs i
    ON t."LocationID" = i.pickup_id;
    -- Results: Manhattan, East Harlem North, Manhattan, East Harlem South, and Manhattan, Morningside Heights
    ```

6. SQL Query:
    ```sql
    SELECT "Zone"
    FROM public.green_taxi g
    INNER JOIN public.taxi_zone t
    ON g."DOLocationID" = t."LocationID"
    WHERE tip_amount = (
         SELECT MAX(tip_amount) AS max_tip
         FROM public.green_taxi g
         INNER JOIN public.taxi_zone t
         ON g."PULocationID" = t."LocationID"
         WHERE "Zone" = 'East Harlem North' AND EXTRACT(MONTH FROM lpep_pickup_datetime) = 10
    );
    ```

