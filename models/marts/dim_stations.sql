with stations as (

      select distinct
          start_station_id    as station_id,
          start_station_name  as station_name,
          start_station_latitude  as latitude,
          start_station_longitude as longitude
      from {{ ref('stg_citibike_trips') }}
      where start_station_id is not null

      union distinct

      select distinct
          end_station_id,
          end_station_name,
          end_station_latitude,
          end_station_longitude
      from {{ ref('stg_citibike_trips') }}
      where end_station_id is not null

  ),

  -- Take one record per station_id, pick the most common name
  deduped as (

      select
          station_id,
          station_name,
          latitude,
          longitude,
          row_number() over (
              partition by station_id
              order by station_name
          ) as rn
      from stations

  )

    select
      station_id,
      station_name,
      latitude,
      longitude
    from deduped
    where rn = 1




--   select * from stations