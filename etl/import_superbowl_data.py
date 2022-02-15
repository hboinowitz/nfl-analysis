import utils
import pandas as pd

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
    superbowls.to_parquet('../data/superbowls.parquet')
    superbowl_stats.to_parquet('../data/superbowl_stats_per_team.parquet')