declare @community_total float, @cur_date datetime;
set @cur_date = getdate();
set @community_total = (select count(event)
                        from community_actions
                        where (event = 'CREATE_COMMUNITY') and (datediff(day, community_registered_time, @cur_date) < 67));

select days, count(days) / @community_total * 100 as prcnt
from (select *
      from (select min(datediff(day, community_registered_time, time) + 1) over(partition by community_id) as days, community_id
            from community_actions
            where datediff(day, @cur_date, time) < 60 and datediff(day, community_registered_time, time) < 7 and event = 'CREATE_CHAT'
           ) as t1
      GROUP by days, community_id
     ) as t2
group by days
ORDER by days;