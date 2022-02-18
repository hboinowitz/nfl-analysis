import utils
import pandas as pd
import locale

def import_superbowl_data():
    ## Load data for all Superbowls
    all_superbowl_tables = utils.get_wiki_table("https://de.wikipedia.org/wiki/Super_Bowl", first = False)
    afl_championships = all_superbowl_tables[0]
    superbowls_nfl = all_superbowl_tables[1]
    superbowl_stats = all_superbowl_tables[2]

    afl_championships = afl_championships.rename({'Siegende Liga':'Siegende Conference', 
                                                'MVP *': 'MVP'}, axis=1)

    # Merge old and new Superbowls
    superbowls = pd.concat([afl_championships, superbowls_nfl])
    superbowls = superbowls.rename(utils.snake_case, axis=1)

    superbowls[['overtime', 'points_winner', 'points_looser']] = superbowls['ergebnis'].apply(utils.parse_result).to_list()
    # Correct hidden zeros
    superbowls.loc[superbowls['points_winner'] < superbowls['points_looser'], 'points_looser'] /= 10
    superbowls['total_points'] = superbowls['points_winner'] + superbowls['points_looser']
    
    # Set locale for parsing dates
    locale.setlocale(locale.LC_ALL, 'de_DE')
    superbowls['datum'] = pd.to_datetime(superbowls['datum'], format='%d. %B %Y')

    superbowls.to_parquet('../data/superbowls.parquet')
    superbowl_stats.to_parquet('../data/superbowl_stats_per_team.parquet')

    team_mapping = utils.team_names_to_mapping(superbowl_stats['Team'])
    team_mapping.to_parquet('../data/team_mapping.parquet')