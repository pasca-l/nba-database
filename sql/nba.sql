drop table playerstats;
drop table matchschedule;
drop table goods;
drop table playerinfo;
drop table teaminfo;

create table playerinfo (playerid int, name varchar, height real, weight real, birthday date, birthplace varchar,
primary key (playerid));
create table playerstats (playerid int, season int, age int, teamid int, league varchar, position varchar, games_played int, games_started int, minutes_played_per_game real, field_goals_per_game real, field_goal_attempts_per_game real, field_goal_percentage real, threepoints_per_game real, threepoint_attempts_per_game real, threepoint_percentage real, twopoints_per_game real, twopoint_attempts_per_game real, twopoint_percentage real, effective_field_goal_percentage real, free_throws_per_game real, free_throw_attempts_per_game real, free_throw_percentage real, offensive_rebounds_per_game real, defensive_rebounds_per_game real, total_rebounds_per_game real, assists_per_game real, steals_per_game real, blocks_per_game real, turnovers_per_game real, personal_fouls_per_game real, points_per_game real,
primary key (playerid, season, teamid), foreign key (playerid) references playerinfo(playerid));
create table teaminfo (teamid int, name varchar, conference varchar, division varchar, coach varchar, abbreviation varchar,
primary key (teamid));
create table matchschedule (start_time timestamp, visitor_teamid int, visitor_score int, home_teamid int, home_score int,
primary key (start_time, visitor_teamid, home_teamid), foreign key (visitor_teamid) references teaminfo(teamid), foreign key (home_teamid) references teaminfo(teamid));
create table goods (goodsid int, reference_teamid int, name varchar, price real,
primary key (goodsid), foreign key (reference_teamid) references teaminfo (teamid));
