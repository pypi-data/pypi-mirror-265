from paladium import Paladium
from rank import Leaderboard

def test():
    # main tests
    api = Paladium()

    # example player
    player = api.get_player('aureliancnx')
    print(player)

    # example faction
    faction = api.get_faction('Insomnium')
    print(faction)
    for member in faction.players:
        print(member)

    # example leaderboard
    leaderboard = api.get_faction_leaderboard()
    for faction in leaderboard:
        print(faction)

    # example player rank
    player_rank = api.get_player_ranks(player=player)
    print(player_rank)

    # example leaderboard: money
    leaderboard_money = api.get_leaderboard(Leaderboard.MONEY)
    for player in leaderboard_money:
        print(player)

if __name__ == '__main__':
    test()