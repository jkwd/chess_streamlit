{% test is_positive_approx(model, column_name, threshold) %}

with dataset as (
    select
    {{ column_name }} as positive_field
    from {{ model }}
)
, validation_errors as (
    -- Get percentage of negative values
    select
    count_if(positive_field < 0) as neg_time
    , count(1) as num_rows
    , count_if(positive_field < 0) / count(1) * 100.0 as perc
    from dataset
)
, check_treshold as (
    -- Check if percentage of negative values is above threshold
    select *
    from validation_errors
    where perc > {{ threshold }}
)
-- Return validation errors if percentage of negative values is above threshold
select *
from check_treshold

{% endtest %}
