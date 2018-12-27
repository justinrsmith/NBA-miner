from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker



db = create_engine(db_string, pool_recycle=600)
base = declarative_base()


class Team(base):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key=True)
    city = Column(String)
    alt_city_name = Column(String)
    full_name = Column(String)
    tricode = Column(String)
    nickname = Column(String)
    url_name = Column(String)
    conf_name = Column(String)
    div_name = Column(String)
    is_nba_franchise = Column(Boolean)
    is_all_star = Column(Boolean)


class Game(base):
    __tablename__ = 'games'

    game_id = Column(Integer, primary_key=True)
    game_date_est = Column(Date)
    season = Column(Integer)
    home_team_id = Column(Integer, ForeignKey(Team.team_id))
    home_pts = Column(Integer)
    visitor_team_id = Column(Integer, ForeignKey(Team.team_id))
    visitor_pts = Column(Integer)
    home_team = relationship('Team', foreign_keys=[home_team_id])
    visitor_team = relationship('Team', foreign_keys=[visitor_team_id])


class ActualGameSpread(base):
    __tablename__ = 'actual_game_spreads'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey(Game.game_id))
    pinnacle_closing = Column(Float)
    pinnacle_moneyline = Column(Integer)
    epoch_datetime = Column(String)
    game = relationship('Game')


class ModelGameSpread(base):
    __tablename__ = 'model_game_spreads'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey(Game.game_id))
    spread = Column(Float)
    game = relationship('Game')


class TotalsDate(base):
    __tablename__ = 'totals_date'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey(Team.team_id))
    date = Column(Date)
    team_name = Column(String)
    gp = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)
    w_pct = Column(Float)
    min = Column(Integer)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    tov = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    blka = Column(Integer)
    pf = Column(Integer)
    pfd = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Integer)
    gp_rank = Column(Integer)
    w_rank = Column(Integer)
    l_rank = Column(Integer)
    w_pct_rank = Column(Integer)
    min_rank = Column(Integer)
    fgm_rank = Column(Integer)
    fga_rank = Column(Integer)
    fg_pct_rank = Column(Integer)
    fg3m_rank = Column(Integer)
    fg3a_rank = Column(Integer)
    fg3_pct_rank = Column(Integer)
    ftm_rank = Column(Integer)
    fta_rank = Column(Integer)
    ft_pct_rank = Column(Integer)
    oreb_rank = Column(Integer)
    dreb_rank = Column(Integer)
    reb_rank = Column(Integer)
    ast_rank = Column(Integer)
    tov_rank = Column(Integer)
    stl_rank = Column(Integer)
    blk_rank = Column(Integer)
    blka_rank = Column(Integer)
    pf_rank = Column(Integer)
    pfd_rank = Column(Integer)
    pts_rank = Column(Integer)
    plus_minus_rank = Column(Integer)
    cfid = Column(Integer)
    cfparams = Column(String)
    team = relationship('Team')


class OpponentTotalsDate(base):
    __tablename__ = 'opponent_totals_date'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey(Team.team_id))
    date = Column(Date)
    team_name = Column(String)
    gp = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)
    w_pct = Column(Float)
    min = Column(Integer)
    opp_fgm = Column(Integer)
    opp_fga = Column(Integer)
    opp_fg_pct = Column(Float)
    opp_fg3m = Column(Integer)
    opp_fg3a = Column(Integer)
    opp_fg3_pct = Column(Float)
    opp_ftm = Column(Integer)
    opp_fta = Column(Integer)
    opp_ft_pct = Column(Float)
    opp_oreb = Column(Integer)
    opp_dreb = Column(Integer)
    opp_reb = Column(Integer)
    opp_ast = Column(Integer)
    opp_tov = Column(Integer)
    opp_stl = Column(Integer)
    opp_blk = Column(Integer)
    opp_blka = Column(Integer)
    opp_pf = Column(Integer)
    opp_pfd = Column(Integer)
    opp_pts = Column(Integer)
    plus_minus = Column(Integer)
    gp_rank = Column(Integer)
    w_rank = Column(Integer)
    l_rank = Column(Integer)
    w_pct_rank = Column(Integer)
    min_rank = Column(Integer)
    opp_fgm_rank = Column(Integer)
    opp_fga_rank = Column(Integer)
    opp_fg_pct_rank = Column(Integer)
    opp_fg3m_rank = Column(Integer)
    opp_fg3a_rank = Column(Integer)
    opp_fg3_pct_rank = Column(Integer)
    opp_ftm_rank = Column(Integer)
    opp_fta_rank = Column(Integer)
    opp_ft_pct_rank = Column(Integer)
    opp_oreb_rank = Column(Integer)
    opp_dreb_rank = Column(Integer)
    opp_reb_rank = Column(Integer)
    opp_ast_rank = Column(Integer)
    opp_tov_rank = Column(Integer)
    opp_stl_rank = Column(Integer)
    opp_blk_rank = Column(Integer)
    opp_blka_rank = Column(Integer)
    opp_pf_rank = Column(Integer)
    opp_pfd_rank = Column(Integer)
    opp_pfd1 = Column(Integer)
    opp_pts_rank = Column(Integer)
    plus_minus_rank = Column(Integer)
    cfid = Column(Integer)
    cfparams = Column(String)
    team = relationship('Team')


class TotalsDateTrending(base):
    __tablename__ = 'totals_date_trending'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey(Team.team_id))
    date = Column(Date)
    team_name = Column(String)
    gp = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)
    w_pct = Column(Float)
    min = Column(Integer)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    tov = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    blka = Column(Integer)
    pf = Column(Integer)
    pfd = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Integer)
    gp_rank = Column(Integer)
    w_rank = Column(Integer)
    l_rank = Column(Integer)
    w_pct_rank = Column(Integer)
    min_rank = Column(Integer)
    fgm_rank = Column(Integer)
    fga_rank = Column(Integer)
    fg_pct_rank = Column(Integer)
    fg3m_rank = Column(Integer)
    fg3a_rank = Column(Integer)
    fg3_pct_rank = Column(Integer)
    ftm_rank = Column(Integer)
    fta_rank = Column(Integer)
    ft_pct_rank = Column(Integer)
    oreb_rank = Column(Integer)
    dreb_rank = Column(Integer)
    reb_rank = Column(Integer)
    ast_rank = Column(Integer)
    tov_rank = Column(Integer)
    stl_rank = Column(Integer)
    blk_rank = Column(Integer)
    blka_rank = Column(Integer)
    pf_rank = Column(Integer)
    pfd_rank = Column(Integer)
    pts_rank = Column(Integer)
    plus_minus_rank = Column(Integer)
    cfid = Column(Integer)
    cfparams = Column(String)
    team = relationship('Team')


class OpponentTotalsDateTrending(base):
    __tablename__ = 'opponent_totals_date_trending'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey(Team.team_id))
    date = Column(Date)
    team_name = Column(String)
    gp = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)
    w_pct = Column(Float)
    min = Column(Integer)
    opp_fgm = Column(Integer)
    opp_fga = Column(Integer)
    opp_fg_pct = Column(Float)
    opp_fg3m = Column(Integer)
    opp_fg3a = Column(Integer)
    opp_fg3_pct = Column(Float)
    opp_ftm = Column(Integer)
    opp_fta = Column(Integer)
    opp_ft_pct = Column(Float)
    opp_oreb = Column(Integer)
    opp_dreb = Column(Integer)
    opp_reb = Column(Integer)
    opp_ast = Column(Integer)
    opp_tov = Column(Integer)
    opp_stl = Column(Integer)
    opp_blk = Column(Integer)
    opp_blka = Column(Integer)
    opp_pf = Column(Integer)
    opp_pfd = Column(Integer)
    opp_pts = Column(Integer)
    plus_minus = Column(Integer)
    gp_rank = Column(Integer)
    w_rank = Column(Integer)
    l_rank = Column(Integer)
    w_pct_rank = Column(Integer)
    min_rank = Column(Integer)
    opp_fgm_rank = Column(Integer)
    opp_fga_rank = Column(Integer)
    opp_fg_pct_rank = Column(Integer)
    opp_fg3m_rank = Column(Integer)
    opp_fg3a_rank = Column(Integer)
    opp_fg3_pct_rank = Column(Integer)
    opp_ftm_rank = Column(Integer)
    opp_fta_rank = Column(Integer)
    opp_ft_pct_rank = Column(Integer)
    opp_oreb_rank = Column(Integer)
    opp_dreb_rank = Column(Integer)
    opp_reb_rank = Column(Integer)
    opp_ast_rank = Column(Integer)
    opp_tov_rank = Column(Integer)
    opp_stl_rank = Column(Integer)
    opp_blk_rank = Column(Integer)
    opp_blka_rank = Column(Integer)
    opp_pf_rank = Column(Integer)
    opp_pfd_rank = Column(Integer)
    opp_pfd1 = Column(Integer)
    opp_pts_rank = Column(Integer)
    plus_minus_rank = Column(Integer)
    cfid = Column(Integer)
    cfparams = Column(String)
    team = relationship('Team')

Session = sessionmaker(db)
session = Session()
