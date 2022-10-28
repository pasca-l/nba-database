drop view highestpoints;
create view highestpoints as
select i.playerid, i.name as playername, s.season, t.teamid, t.name as teamname, s.points_per_game
from playerinfo i, playerstats s, teaminfo t
where i.playerid=s.playerid and s.teamid=t.teamid and s.season>2015 and s.points_per_game>25
order by s.points_per_game desc;

drop view matchschedule_withname;
create view matchschedule_withname as
select m.start_time, m.home_teamid, home.name as home, m.home_score, m.visitor_teamid, visitor.name as visitor, m.visitor_score
from matchschedule m
left outer join teaminfo home on m.home_teamid=home.teamid
left outer join teaminfo visitor on m.visitor_teamid=visitor.teamid;
