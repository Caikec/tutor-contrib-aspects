with videos as (
    {% include 'openedx-assets/queries/dim_course_videos.sql' %}
), transcripts as (
    select
        emission_time,
        org,
        splitByString('/', course_id)[-1] as course_key,
        video_id,
        actor_id
    from
        {{ DBT_PROFILE_TARGET_DATABASE }}.transcript_usage
    {% raw -%}
    {% if filter_values('org') != [] %}
    where
        org in {{ filter_values('org') | where_in }}
    {% endif %}
    {%- endraw %}
)

select
    transcripts.emission_time as emission_time,
    transcripts.org as org,
    videos.course_name as course_name,
    videos.run_name as run_name,
    videos.video_name as video_name,
    transcripts.actor_id as actor_id
from
    transcripts
    join videos
        using (org, course_key, video_id)
