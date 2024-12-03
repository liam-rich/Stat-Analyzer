import unittest
from unittest.mock import Mock, patch
import os
import sys

# Add the parent directory to the path so we can import nba_analyzer
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from nba_analyzer import search_player, get_player_stats, display_player_stats

class TestNBAAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.sample_player_data = {
            'info': {
                'name': 'LeBron James',
                'team': 'Los Angeles Lakers',
                'position': 'F',
                'height': '6-9',
                'weight': '250',
                'country': 'USA',
                'experience': 19,
                'draft_year': '2003',
                'jersey': '23'
            },
            'recent_games': [
                {
                    'GAME_DATE': 'DEC 25, 2023',
                    'PTS': 30,
                    'REB': 10,
                    'AST': 8,
                    'STL': 2,
                    'BLK': 1,
                    'MIN': '36',
                    'FGM': 12,
                    'FGA': 20,
                    'FG_PCT': 0.600,
                    'FG3M': 2,
                    'FG3A': 5,
                    'FG3_PCT': 0.400,
                    'FTM': 4,
                    'FTA': 5,
                    'FT_PCT': 0.800
                }
            ]
        }

    @patch('nba_api.stats.static.players.find_players_by_full_name')
    def test_search_player_valid_name(self, mock_find_players):
        """Test searching for a valid player name"""
        mock_find_players.return_value = [{'full_name': 'LeBron James', 'id': 2544}]
        result = search_player('LeBron James')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['full_name'], 'LeBron James')

    @patch('nba_api.stats.static.players.find_players_by_full_name')
    def test_search_player_invalid_name(self, mock_find_players):
        """Test searching for an invalid player name"""
        mock_find_players.return_value = []
        result = search_player('Invalid Player')
        self.assertEqual(len(result), 0)

    def test_error_handling_empty_name(self):
        """Test handling empty player name"""
        result = search_player('')
        self.assertEqual(len(result), 0)

    def test_error_handling_special_chars(self):
        """Test handling special characters in name"""
        result = search_player('!@#$%')
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()