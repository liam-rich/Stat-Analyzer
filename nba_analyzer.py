from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playergamelog, playercareerstats
from datetime import datetime

def search_player(player_name):
    """Search for a player by name"""
    try:
        player_list = players.find_players_by_full_name(player_name)
        if not player_list:
            raise ValueError('No players found. Try using the player\'s full name.')
        return player_list
    except Exception as e:
        print(f'Error searching for player: {str(e)}')
        return []

def get_player_stats(player_id):
    """Get comprehensive player stats"""
    try:
        # Get player info
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        info = player_info.get_normalized_dict()['CommonPlayerInfo'][0]
        
        # Get recent games
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season='2023-24')
        games = game_log.get_normalized_dict()['PlayerGameLog']
        
        # Get career stats
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_stats = career.get_normalized_dict()
        
        recent_games = games[:5] if games else []
        
        # Calculate recent averages
        if recent_games:
            recent_averages = {
                'points': sum(game['PTS'] for game in recent_games) / len(recent_games),
                'rebounds': sum(game['REB'] for game in recent_games) / len(recent_games),
                'assists': sum(game['AST'] for game in recent_games) / len(recent_games),
                'steals': sum(game['STL'] for game in recent_games) / len(recent_games),
                'blocks': sum(game['BLK'] for game in recent_games) / len(recent_games),
                'fg_pct': sum(game['FG_PCT'] for game in recent_games) / len(recent_games),
                'fg3_pct': sum(game['FG3_PCT'] for game in recent_games) / len(recent_games),
                'ft_pct': sum(game['FT_PCT'] for game in recent_games) / len(recent_games),
            }
        else:
            recent_averages = None

        return {
            'info': {
                'name': f"{info['FIRST_NAME']} {info['LAST_NAME']}",
                'team': info['TEAM_NAME'],
                'position': info['POSITION'],
                'height': info['HEIGHT'],
                'weight': info['WEIGHT'],
                'country': info['COUNTRY'],
                'experience': info['SEASON_EXP'],
                'draft_year': info['DRAFT_YEAR'],
                'jersey': info.get('JERSEY', 'N/A')
            },
            'recent_games': recent_games,
            'recent_averages': recent_averages,
            'season_by_season': career_stats['SeasonTotalsRegularSeason'],
            'career_totals': career_stats['CareerTotalsRegularSeason'][0] if career_stats['CareerTotalsRegularSeason'] else None
        }
    except Exception as e:
        print(f'Error getting player stats: {str(e)}')
        return None

def display_player_stats(stats):
    """Display comprehensive player stats"""
    if not stats:
        print("No stats available")
        return
        
    # Display basic info
    info = stats['info']
    print("\nPlayer Details:")
    print("=" * 50)
    print(f"Name: {info['name']}")
    print(f"Team: {info['team']}")
    print(f"Position: {info['position']}")
    print(f"Height: {info['height']}")
    print(f"Weight: {info['weight']}")
    print(f"Country: {info['country']}")
    print(f"Experience: {info['experience']} years")
    print(f"Draft Year: {info['draft_year']}")
    print(f"Jersey Number: {info['jersey']}")

    # Display recent averages
    if stats['recent_averages']:
        print("\nRecent Averages (Last 5 Games):")
        print("=" * 50)
        ra = stats['recent_averages']
        print(f"Points: {ra['points']:.1f}")
        print(f"Rebounds: {ra['rebounds']:.1f}")
        print(f"Assists: {ra['assists']:.1f}")
        print(f"Steals: {ra['steals']:.1f}")
        print(f"Blocks: {ra['blocks']:.1f}")
        print(f"FG%: {ra['fg_pct']*100:.1f}%")
        print(f"3P%: {ra['fg3_pct']*100:.1f}%")
        print(f"FT%: {ra['ft_pct']*100:.1f}%")
    
    # Display last game
    if stats['recent_games']:
        print("\nLast Game Performance:")
        print("=" * 50)
        lg = stats['recent_games'][0]
        print(f"Date: {lg['GAME_DATE']}")
        print(f"Points: {lg['PTS']}")
        print(f"Rebounds: {lg['REB']}")
        print(f"Assists: {lg['AST']}")
        print(f"Steals: {lg['STL']}")
        print(f"Blocks: {lg['BLK']}")
        print(f"Minutes: {lg['MIN']}")
        print(f"FG: {lg['FGM']}/{lg['FGA']} ({lg['FG_PCT']*100:.1f}%)")
        print(f"3P: {lg['FG3M']}/{lg['FG3A']} ({lg['FG3_PCT']*100:.1f}%)")
        print(f"FT: {lg['FTM']}/{lg['FTA']} ({lg['FT_PCT']*100:.1f}%)")
    
    # Display career stats
    if stats['career_totals']:
        print("\nCareer Averages:")
        print("=" * 50)
        ct = stats['career_totals']
        games_played = ct['GP']
        print(f"Games Played: {games_played}")
        print(f"Points: {ct['PTS']/games_played:.1f}")
        print(f"Rebounds: {ct['REB']/games_played:.1f}")
        print(f"Assists: {ct['AST']/games_played:.1f}")
        print(f"Steals: {ct['STL']/games_played:.1f}")
        print(f"Blocks: {ct['BLK']/games_played:.1f}")
        print(f"FG%: {ct['FG_PCT']*100:.1f}%")
        print(f"3P%: {ct['FG3_PCT']*100:.1f}%")
        print(f"FT%: {ct['FT_PCT']*100:.1f}%")
        
        # Career totals
        print("\nCareer Totals:")
        print("=" * 50)
        print(f"Total Points: {ct['PTS']}")
        print(f"Total Rebounds: {ct['REB']}")
        print(f"Total Assists: {ct['AST']}")
        print(f"Total Steals: {ct['STL']}")
        print(f"Total Blocks: {ct['BLK']}")
        print(f"Games Played: {ct['GP']}")
        print(f"Minutes Played: {ct['MIN']}")

def main():
    print("Welcome to NBA Stats Analyzer!")
    print("Loading data...")
    
    while True:
        print("\nNBA Stats Analyzer")
        print("1. Search for a player")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        
        try:
            if choice == '1':
                name = input('Enter player name (or "back" to return): ')
                if name.lower() == 'back':
                    continue
                    
                print('Searching...')
                players_found = search_player(name)
                
                if players_found:
                    print('\nFound Players:')
                    for i, player in enumerate(players_found, 1):
                        print(f"{i}. {player['full_name']}")
                    
                    choice = input('\nSelect a player number (or "back" to return): ')
                    if choice.lower() == 'back':
                        continue
                        
                    try:
                        index = int(choice) - 1
                        if 0 <= index < len(players_found):
                            print("\nFetching comprehensive player stats...")
                            stats = get_player_stats(players_found[index]['id'])
                            display_player_stats(stats)
                        else:
                            print('Invalid selection.')
                    except ValueError:
                        print('Invalid input. Please enter a number.')
                else:
                    print('No players found.')
                    
            elif choice == '2':
                print('Thanks for using NBA Stats Analyzer!')
                break
                
            else:
                print('Invalid choice. Please try again.')
                
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            
        input('\nPress Enter to continue...')

if __name__ == '__main__':
    main()