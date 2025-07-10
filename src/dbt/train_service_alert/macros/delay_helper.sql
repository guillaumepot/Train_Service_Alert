{% macro normalize_delay(delay) %}
  CASE WHEN {{ delay }} IS NULL THEN 0 ELSE {{ delay }} END
{% endmacro %}