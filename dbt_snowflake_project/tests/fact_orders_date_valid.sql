SELECT *
from {{ ref('fact_orders') }}
where order_date < '2022-12-31' or order_date > CURRENT_DATE();