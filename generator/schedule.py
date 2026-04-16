def get_match_time_slot(row_idx, round_idx):
    """
    Returns True if row_idx is the first slot of a match in round_idx.
    round_idx is 0-indexed.
    """
    spacing = 2 ** (round_idx + 1)
    return (row_idx % spacing) == 0

def get_advancing_bye(sl_no, n_players):
    """
    Returns True if this SL NO automatically advances in Round 1 because its 
    opponent is a BYE.
    Pairs in R1: (1,2), (3,4)...
    If sl_no is odd and sl_no + 1 is a bye (sl_no + 1 > n_players)
    If sl_no is even and sl_no - 1 is a bye (sl_no - 1 > n_players)
    """
    partner = sl_no + 1 if sl_no % 2 != 0 else sl_no - 1
    return partner > n_players and sl_no <= n_players
