    {{ config(                                                                                                                                                                        
      materialized='table',                                                                                                                                                         
      partition_by={                                                                                                                                                                
        "field": "starttime",                                                                                                                                                       
        "data_type": "timestamp",                                                                                                                                                 
        "granularity": "day"                                                                                                                                                      
      }                                                                                                                                                                             
  ) }}    

with trips as (
                                                                                                                                                                                    
      select * from {{ ref('stg_citibike_trips') }}
                                                                                                                                                                                    
  ),                                                        
                                                                                                                                                                                    
  start_stations as (
                                                                                                                                                                                    
      select * from {{ ref('dim_stations') }}               

  ),                                          
                                          
  final as (
                                                                                                                                                                                    
      select
          -- trip core                                                                                                                                                              
          t.bikeid,                                         
          t.starttime,
          t.stoptime,                         
          t.tripduration,                 
          t.tripduration_minutes,
                                                                                                                                                                                    
          -- time dimensions              
          t.trip_year,                                                                                                                                                              
          t.trip_month,                                                                                                                                                             
          t.trip_day_of_week,
          t.trip_hour,                                                                                                                                                              
          t.is_weekend,                                     
                                          
          -- start station
          t.start_station_id,                                                                                                                                                       
          t.start_station_name,
          s.latitude   as start_latitude,                                                                                                                                           
          s.longitude  as start_longitude,                  
                                          
          -- end station
          t.end_station_id,                                                                                                                                                         
          t.end_station_name,
                                                                                                                                                                                    
          -- rider                                          
          t.usertype,                     
          t.gender,
          t.birth_year,                                                                                                                                                             
   
          -- derived KPIs                                                                                                                                                           
          case                                              
              when t.tripduration_minutes < 10  then 'short'
              when t.tripduration_minutes < 30  then 'medium'
              else 'long'                     
          end as trip_length_category     
                                                                                                                                                                                    
      from trips t                                                                                                                                                                  
      left join start_stations s                                                                                                                                                    
          on t.start_station_id = s.station_id                                                                                                                                      
                                                            
  )                                                           
            
  select * from final    