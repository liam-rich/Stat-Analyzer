import unittest
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.append(str(Path(__file__).parent.parent))
from nba_analyzer import search_player, get_player_stats, display_player_stats

class TestNBAAnalyzerIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_full_player_workflow(self):
        """Test complete workflow from search to display"""
        # Search for a known player
        players = search_player('LeBron James')
        self.assertTrue(len(players) > 0)
        
        # Get stats for the first player found
        player_id = players[0]['id']
        stats = get_player_stats(player_id)
        
        # Verify all required data is present
        self.assertIsNotNone(stats)
        self.assertIn('info', stats)
        self.assertIn('recent_games', stats)
        
        # Check basic information
        info = stats['info']
        self.assertIn('name', info)
        self.assertIn('team', info)
        self.assertIn('position', info)

    def test_multiple_player_search(self):
        """Test searching and processing multiple players"""
        test_names = ['James', 'Curry', 'Giannis']
        
        for name in test_names:
            players = search_player(name)
            self.assertTrue(len(players) > 0)
            
            # Test first player in each search
            stats = get_player_stats(players[0]['id'])
            self.assertIsNotNone(stats)

    @patch('builtins.input', side_effect=['1'])
    def test_player_selection(self, mock_input):
        """Test player selection from multiple results"""
        players = search_player('James')
        self.assertTrue(len(players) > 1)  # Should find multiple James

    def test_network_failure(self):
        """Test handling of network failures"""
        with patch('nba_api.stats.static.players.find_players_by_full_name', 
                  side_effect=Exception('Network Error')):
            result = search_player('LeBron James')
            self.assertEqual(len(result), 0)

    def test_stats_calculation_accuracy(self):
        """Test accuracy of statistical calculations"""
        players = search_player('LeBron James')
        if players:
            stats = get_player_stats(players[0]['id'])
            
            # Verify recent games calculations
            if stats and 'recent_games' in stats and stats['recent_games']:
                recent_games = stats['recent_games']
                
                # Verify basic stat ranges
                for game in recent_games:
                    self.assertGreaterEqual(game['PTS'], 0)
                    self.assertLess(game['PTS'], 100)  # No one scores 100+ in a game
                    self.assertGreaterEqual(game['REB'], 0)
                    self.assertGreaterEqual(game['AST'], 0)

    def test_invalid_inputs(self):
        """Test system handling of various invalid inputs"""
        test_cases = [
            '',  # Empty string
            ' ',  # Whitespace
            'a' * 100,  # Very long name
            '12345',  # Numbers only
            '!@#$%'  # Special characters
        ]
        
        for test_input in test_cases:
            result = search_player(test_input)
            # Should return empty list but not crash
            self.assertEqual(type(result), list)

if __name__ == '__main__':
    unittest.main()