from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playergamelog, playercareerstats
from datetime import datetime

def search_player(player_name):
    """Search for a player by name"""
    try:
        # Validate input
        if not player_name or not player_name.strip():
            return []

        # Remove special characters and validate
        cleaned_name = ''.join(c for c in player_name if c.isalnum() or c.isspace())
        if not cleaned_name:
            return []

        player_list = players.find_players_by_full_name(cleaned_name)
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

def compare_players(player1_stats, player2_stats):
    """Compare stats between two players"""
    if not player1_stats or not player2_stats:
        print("Cannot compare - stats missing for one or both players")
        return
        
    print("\nPlayer Comparison:")
    print("=" * 70)
    p1 = player1_stats['info']
    p2 = player2_stats['info']
    
    # Basic Info Comparison
    print(f"{'Attribute':<20} {p1['name']:<25} {p2['name']:<25}")
    print("-" * 70)
    print(f"{'Position':<20} {p1['position']:<25} {p2['position']:<25}")
    print(f"{'Team':<20} {p1['team']:<25} {p2['team']:<25}")
    print(f"{'Experience':<20} {p1['experience']:<25} {p2['experience']:<25}")
    
    # Recent Averages Comparison
    if player1_stats['recent_averages'] and player2_stats['recent_averages']:
        print("\nRecent Averages (Last 5 Games):")
        print("-" * 70)
        ra1 = player1_stats['recent_averages']
        ra2 = player2_stats['recent_averages']
        
        print(f"{'Points':<20} {ra1['points']:>6.1f}{' ':>19} {ra2['points']:>6.1f}{' ':>19}")
        print(f"{'Rebounds':<20} {ra1['rebounds']:>6.1f}{' ':>19} {ra2['rebounds']:>6.1f}{' ':>19}")
        print(f"{'Assists':<20} {ra1['assists']:>6.1f}{' ':>19} {ra2['assists']:>6.1f}{' ':>19}")
        print(f"{'Steals':<20} {ra1['steals']:>6.1f}{' ':>19} {ra2['steals']:>6.1f}{' ':>19}")
        print(f"{'Blocks':<20} {ra1['blocks']:>6.1f}{' ':>19} {ra2['blocks']:>6.1f}{' ':>19}")
        print(f"{'FG%':<20} {ra1['fg_pct']*100:>6.1f}%{' ':>18} {ra2['fg_pct']*100:>6.1f}%{' ':>18}")
        print(f"{'3P%':<20} {ra1['fg3_pct']*100:>6.1f}%{' ':>18} {ra2['fg3_pct']*100:>6.1f}%{' ':>18}")
        print(f"{'FT%':<20} {ra1['ft_pct']*100:>6.1f}%{' ':>18} {ra2['ft_pct']*100:>6.1f}%{' ':>18}")
    
    # Career Comparison
    if player1_stats['career_totals'] and player2_stats['career_totals']:
        print("\nCareer Averages:")
        print("-" * 70)
        ct1 = player1_stats['career_totals']
        ct2 = player2_stats['career_totals']
        gp1 = ct1['GP']
        gp2 = ct2['GP']
        
        print(f"{'Games Played':<20} {ct1['GP']:>6}{' ':>19} {ct2['GP']:>6}{' ':>19}")
        print(f"{'Points':<20} {ct1['PTS']/gp1:>6.1f}{' ':>19} {ct2['PTS']/gp2:>6.1f}{' ':>19}")
        print(f"{'Rebounds':<20} {ct1['REB']/gp1:>6.1f}{' ':>19} {ct2['REB']/gp2:>6.1f}{' ':>19}")
        print(f"{'Assists':<20} {ct1['AST']/gp1:>6.1f}{' ':>19} {ct2['AST']/gp2:>6.1f}{' ':>19}")
        print(f"{'Steals':<20} {ct1['STL']/gp1:>6.1f}{' ':>19} {ct2['STL']/gp2:>6.1f}{' ':>19}")
        print(f"{'Blocks':<20} {ct1['BLK']/gp1:>6.1f}{' ':>19} {ct2['BLK']/gp2:>6.1f}{' ':>19}")
        print(f"{'FG%':<20} {ct1['FG_PCT']*100:>6.1f}%{' ':>18} {ct2['FG_PCT']*100:>6.1f}%{' ':>18}")
        print(f"{'3P%':<20} {ct1['FG3_PCT']*100:>6.1f}%{' ':>18} {ct2['FG3_PCT']*100:>6.1f}%{' ':>18}")
        print(f"{'FT%':<20} {ct1['FT_PCT']*100:>6.1f}%{' ':>18} {ct2['FT_PCT']*100:>6.1f}%{' ':>18}")
        
        # Career Totals
        print("\nCareer Totals:")
        print("-" * 70)
        print(f"{'Total Points':<20} {ct1['PTS']:>6}{' ':>19} {ct2['PTS']:>6}{' ':>19}")
        print(f"{'Total Rebounds':<20} {ct1['REB']:>6}{' ':>19} {ct2['REB']:>6}{' ':>19}")
        print(f"{'Total Assists':<20} {ct1['AST']:>6}{' ':>19} {ct2['AST']:>6}{' ':>19}")
        print(f"{'Total Steals':<20} {ct1['STL']:>6}{' ':>19} {ct2['STL']:>6}{' ':>19}")
        print(f"{'Total Blocks':<20} {ct1['BLK']:>6}{' ':>19} {ct2['BLK']:>6}{' ':>19}")

def main():
    print("Welcome to NBA Stats Analyzer!")
    print("Loading data...")
    
    while True:
        print("\nNBA Stats Analyzer")
        print("1. Search for a player")
        print("2. Compare two players")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
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
                            plot_player_stats(stats)
                        else:
                            print('Invalid selection.')
                    except ValueError:
                        print('Invalid input. Please enter a number.')
                else:
                    print('No players found.')
            
            elif choice == '2':
                # First player
                name1 = input('Enter first player name: ')
                players1 = search_player(name1)
                if not players1:
                    print('No players found.')
                    continue
                
                print('\nFound Players:')
                for i, player in enumerate(players1, 1):
                    print(f"{i}. {player['full_name']}")
                
                choice1 = input('Select first player number: ')
                try:
                    index1 = int(choice1) - 1
                    if not (0 <= index1 < len(players1)):
                        print('Invalid selection.')
                        continue
                except ValueError:
                    print('Invalid input.')
                    continue
                
                # Second player
                name2 = input('Enter second player name: ')
                players2 = search_player(name2)
                if not players2:
                    print('No players found.')
                    continue
                
                print('\nFound Players:')
                for i, player in enumerate(players2, 1):
                    print(f"{i}. {player['full_name']}")
                
                choice2 = input('Select second player number: ')
                try:
                    index2 = int(choice2) - 1
                    if not (0 <= index2 < len(players2)):
                        print('Invalid selection.')
                        continue
                except ValueError:
                    print('Invalid input.')
                    continue
                
                print("\nFetching stats for comparison...")
                stats1 = get_player_stats(players1[index1]['id'])
                stats2 = get_player_stats(players2[index2]['id'])
                compare_players(stats1, stats2)
                plot_comparison(stats1, stats2)
                    
            elif choice == '3':
                print('Thanks for using NBA Stats Analyzer!')
                break
                
            else:
                print('Invalid choice. Please try again.')
                
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            
        input('\nPress Enter to continue...')

import matplotlib.pyplot as plt

def plot_player_stats(stats):
    """Graphically illustrate a player's recent averages as bar charts, saved to files."""
    if not stats or not stats['recent_averages']:
        print("No stats available to plot.")
        return

    averages = stats['recent_averages']
    categories = list(averages.keys())
    values = list(averages.values())

    # Separate percentages and other stats
    percentage_categories = ['fg_pct', 'fg3_pct', 'ft_pct']
    percentage_values = [averages[c] * 100 for c in percentage_categories if c in averages]
    other_categories = [c for c in categories if c not in percentage_categories]
    other_values = [averages[c] for c in other_categories]

    # Plot other stats
    plt.figure(figsize=(10, 6))
    plt.bar(other_categories, other_values, color='blue', alpha=0.7)
    plt.title(f"{stats['info']['name']} - Recent Averages (Counts)", fontsize=16)
    plt.xlabel("Stat Categories", fontsize=14)
    plt.ylabel("Values", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    count_file = f"{stats['info']['name'].replace(' ', '_').lower()}_recent_averages_counts.png"
    plt.savefig(count_file)
    print(f"Counts plot saved as {count_file}")
    plt.close()

    # Plot percentages
    plt.figure(figsize=(8, 6))
    plt.bar(percentage_categories, percentage_values, color='green', alpha=0.7)
    plt.title(f"{stats['info']['name']} - Recent Averages (Percentages)", fontsize=16)
    plt.xlabel("Stat Categories", fontsize=14)
    plt.ylabel("Percentage (%)", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    percent_file = f"{stats['info']['name'].replace(' ', '_').lower()}_recent_averages_percentages.png"
    plt.savefig(percent_file)
    print(f"Percentages plot saved as {percent_file}")
    plt.close()


def plot_comparison(player1_stats, player2_stats):
    """Graphically compare two players' recent averages and career averages, saved to files."""
    if not player1_stats or not player2_stats:
        print("Cannot compare - stats missing for one or both players.")
        return

    if not player1_stats['recent_averages'] or not player2_stats['recent_averages']:
        print("No recent averages available to compare.")
        return

    # Extract stats
    averages1 = player1_stats['recent_averages']
    averages2 = player2_stats['recent_averages']

    categories = list(averages1.keys())
    percentage_categories = ['fg_pct', 'fg3_pct', 'ft_pct']
    other_categories = [c for c in categories if c not in percentage_categories]

    # Values for other stats
    other_values1 = [averages1[c] for c in other_categories]
    other_values2 = [averages2[c] for c in other_categories]

    # Values for percentages
    percentage_values1 = [averages1[c] * 100 for c in percentage_categories]
    percentage_values2 = [averages2[c] * 100 for c in percentage_categories]

    # Plot other stats comparison
    x = range(len(other_categories))
    plt.figure(figsize=(12, 6))
    plt.bar(x, other_values1, width=0.4, label=player1_stats['info']['name'], color='blue', alpha=0.7)
    plt.bar([i + 0.4 for i in x], other_values2, width=0.4, label=player2_stats['info']['name'], color='orange', alpha=0.7)
    plt.title("Comparison of Recent Averages (Counts)", fontsize=16)
    plt.xlabel("Stat Categories", fontsize=14)
    plt.ylabel("Values", fontsize=14)
    plt.xticks([i + 0.2 for i in x], other_categories, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    count_file = f"{player1_stats['info']['name'].replace(' ', '_').lower()}_vs_{player2_stats['info']['name'].replace(' ', '_').lower()}_counts_comparison.png"
    plt.savefig(count_file)
    print(f"Counts comparison plot saved as {count_file}")
    plt.close()

    # Plot percentages comparison
    x = range(len(percentage_categories))
    plt.figure(figsize=(10, 6))
    plt.bar(x, percentage_values1, width=0.4, label=player1_stats['info']['name'], color='green', alpha=0.7)
    plt.bar([i + 0.4 for i in x], percentage_values2, width=0.4, label=player2_stats['info']['name'], color='purple', alpha=0.7)
    plt.title("Comparison of Recent Averages (Percentages)", fontsize=16)
    plt.xlabel("Stat Categories", fontsize=14)
    plt.ylabel("Percentage (%)", fontsize=14)
    plt.xticks([i + 0.2 for i in x], percentage_categories, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    percent_file = f"{player1_stats['info']['name'].replace(' ', '_').lower()}_vs_{player2_stats['info']['name'].replace(' ', '_').lower()}_percentages_comparison.png"
    plt.savefig(percent_file)
    print(f"Percentages comparison plot saved as {percent_file}")
    plt.close()




if __name__ == '__main__':
    main()