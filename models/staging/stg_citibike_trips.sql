with source as (                                                                                                                                                                  
                                                                                                                                                                                    
      select *
      from `bigquery-public-data.new_york_citibike.citibike_trips`                                                                                                                  
      where tripduration is not null                        
        and tripduration > 0                                                                                                                                                        
                                                            
  ),                                                                                                                                                                                
   
  cleaned as (                                                                                                                                                                      
                                                            
      select                                                                                                                                                                        
          -- trip identifiers                               
          bikeid,
                                              
          -- timestamps                   
          starttime,
          stoptime,                                                                                                                                                                 
   
          -- trip duration                                                                                                                                                          
          tripduration,                                     
          round(tripduration / 60, 2) as tripduration_minutes,
                                              
          -- start station                
          start_station_id,
          start_station_name,                                                                                                                                                       
          start_station_latitude,         
          start_station_longitude,                                                                                                                                                  
                                                                                                                                                                                    
          -- end station
          end_station_id,                                                                                                                                                           
          end_station_name,                                 
          end_station_latitude,
          end_station_longitude,
                                              
          -- rider info                   
          usertype,
          coalesce(cast(birth_year as string), 'unknown') as birth_year,                                                                                                            
          gender,                             
                                                                                                                                                                                    
          -- derived fields                                 
          extract(year from starttime)        as trip_year,                                                                                                                         
          extract(month from starttime)       as trip_month,
          extract(dayofweek from starttime)   as trip_day_of_week,                                                                                                                  
          extract(hour from starttime)        as trip_hour, 
          case                                                                                                                                                                      
              when extract(dayofweek from starttime) in (1, 7) then true
              else false                                                                                                                                                            
          end as is_weekend                                 
                                                                                                                                                                                    
      from source                                                                                                                                                                   
   
  )                                                                                                                                                                                 
                                                            
  select * from cleaned