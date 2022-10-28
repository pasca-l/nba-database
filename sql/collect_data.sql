select h.*, g.name as goods_name, g.price
from highestspoints h, goods g, teaminfo t
where h.teamname=t.name and t.teamid=g.reference_teamid and g.name='jersey';
