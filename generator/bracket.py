import math

def get_bracket_size(num_players):
    """
    Returns the next power of 2 for a given number of players.
    Example: 20 -> 32
    """
    if num_players < 2:
        return 2
    return 1 << (num_players - 1).bit_length()

def get_round_names(bracket_size):
    """
    Returns the round names based on the bracket size.
    Mapping logic:
    - Last 4 rounds: Finals, SF, QF, PQF (if applicable)
    - Earlier rounds: I, II, III...
    """
    if bracket_size < 2:
        return ["Finals"]

    # Dynamic round headers by bracket size:
    # 32 -> I, PQF, QF, SF, Finals
    # 64 -> I, II, PQF, QF, SF, Finals
    # 128 -> I, II, III, PQF, QF, SF, Finals
    num_rounds = int(math.log2(bracket_size))
    early_count = max(0, num_rounds - 4)
    roman = ["I", "II", "III", "IV", "V", "VI", "VII"]
    names = roman[:early_count]

    tail = ["PQF", "QF", "SF", "Finals"]
    names.extend(tail[-min(4, num_rounds):])
    return names

def get_seeding_order(n):
    """
    Returns the standard seeding order for N slots (where N is a power of 2).
    Example for 8: [0, 7, 4, 3, 2, 5, 6, 1]
    """
    if n == 1:
        return [0]
    
    seeds = [0, 1]
    while len(seeds) < n:
        new_seeds = []
        for s in seeds:
            new_seeds.append(s)
            new_seeds.append(2 * len(seeds) - 1 - s)
        seeds = new_seeds
    return seeds

def generate_bracket_data(n_players):
    """
    Generates initial bracket structure.
    Byes are distributed based on standard seeding (top recipient gets first bye, etc.)
    Wait, in tournament logic, top seeds get byes. 
    So for 20 players in 32, the 12 players with worst seeds get NO byes, or the 12 best get them?
    Usually, BYEs are the 'missing' players.
    If we have 32 slots and 20 players, we have 12 empty slots (BYEs).
    The best seeds (1, 2, etc.) should be PAIRED with these empty slots.
    """
    bracket_size = get_bracket_size(n_players)
    num_byes = bracket_size - n_players
    round_names = get_round_names(bracket_size)
    
    # Seeding order for 32: [0, 31, 16, 15, ...]
    # The first 12 slots in this order will be paired with BYEs.
    # No, the first 'n_players' slots in this order get REAL players.
    # The remaining 'num_byes' slots from the end of the seeding order are BYEs.
    # Wait:
    # If 1 is best seed, he is at 0. Bye recipient.
    # If 2 is second best, he is at 1. Bye recipient.
    # ...
    # Slots that have a BYE in R1.
    
    seeding = get_seeding_order(bracket_size)
    
    # We'll place players into the seeding order slots.
    # Top 'n_players' of the seeding order are the real players.
    # BUT we want to keep the SL NO (1 to 20) sequential in the final table?
    # No, the table should be SL 1 to 32.
    # Let's decide which SL get a player.
    
    player_slots = set(seeding[:n_players])
    
    players = []
    for i in range(bracket_size):
        sl = i + 1
        is_bye = i not in player_slots
        players.append({
            "sl": sl,
            "name": "",
            "inst": "",
            "is_bye": is_bye
        })
    
    return {
        "bracket_size": bracket_size,
        "num_byes": num_byes,
        "round_names": round_names,
        "players": players
    }
