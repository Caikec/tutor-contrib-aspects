with courses as (
    {% include 'openedx-assets/queries/dim_courses.sql' %}
), video_blocks as (
    select
        org,
        course_key,
        location as video_id,
        display_name as video_name
    from
        {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }}
    where
    {% raw -%}
        JSON_VALUE(xblock_data_json, '$.block_type') = 'video'
        {% if filter_values('org') != [] %}
        and org in {{ filter_values('org') | where_in }}
        {% endif %}
    {%- endraw %}
)

select
    courses.org as org,
    courses.course_name as course_name,
    courses.course_key as course_key,
    courses.run_name as run_name,
    video_blocks.video_id as video_id,
    video_blocks.video_name as video_name
from
    courses
    join video_blocks
        using (course_key)
