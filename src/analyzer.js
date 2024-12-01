
import readline from 'readline-sync';
import fetch from 'node-fetch';
import asciichart from 'asciichart';

// Configuration
const API_BASE = 'https://www.balldontlie.io/api/v1/';

/**
 * Search for a player by name
 * @param {string} playerName - Name to search for
 * @returns {Array} Array of matching players
 */
async function searchPlayer(playerName) {
    try {
        const response = await fetch(`${API_BASE}players?search=${playerName}`);
        const data = await response.json();
        return data.data.map(player => ({
            id: player.id,
            name: `${player.first_name} ${player.last_name}`,
            team: player.team.full_name
        }));
    } catch (error) {
        console.error('Error searching for player:', error);
        return [];
    }
}

/**
 * Get statistics for a specific player
 * @param {number} playerID - Player's ID
 * @returns {Array} Array of game statistics
 */
async function getPlayerStats(playerID) {
    try {
        const response = await fetch(`${API_BASE}stats?player_ids[]=${playerID}&per_page=82`);
        const data = await response.json();
        return data.data
            .map(game => ({
                date: game.game.date,
                points: game.pts || 0,
                assists: game.ast || 0,
                rebounds: game.reb || 0
            }))
            .sort((a, b) => new Date(b.date) - new Date(a.date));
    } catch (error) {
        console.error('Error getting player stats:', error);
        return [];
    }
}

/**
 * Display a graph of statistics
 * @param {Array} stats - Array of game statistics
 * @param {string} statType - Type of statistic to display
 */
function displayStatsGraph(stats, statType) {
    const values = stats.map(game => game[statType]);
    console.log(`\n${statType.toUpperCase()} OVER LAST ${values.length} GAMES:`);
    console.log(asciichart.plot(values, { height: 10 }));
    
    const average = values.reduce((a, b) => a + b) / values.length;
    console.log(`\nAverage ${statType}: ${average.toFixed(1)}`);
}

/**
 * Main application loop
 */
async function main() {
    while (true) {
        console.clear();
        
        const playerName = readline.question('Enter player name (or "exit" to quit): ');
        if (playerName.toLowerCase() === 'exit') break;

        console.log('\nSearching...');
        const players = await searchPlayer(playerName);

        if (players.length === 0) {
            console.log('No players found.');
            readline.question('Press Enter to try again...');
            continue;
        }

        let selectedPlayer;
        if (players.length > 1) {
            console.log('\nMultiple players found:');
            players.forEach((player, index) => {
                console.log(`${index + 1}. ${player.name} (${player.team})`);
            });
            const choice = readline.questionInt('Select player number: ', {
                limit: input => input > 0 && input <= players.length
            });
            selectedPlayer = players[choice - 1];
        } else {
            selectedPlayer = players[0];
        }

        console.log(`\nGetting stats for ${selectedPlayer.name}...`);
        const stats = await getPlayerStats(selectedPlayer.id);

        if (stats.length === 0) {
            console.log('No stats available.');
            readline.question('Press Enter to try again...');
            continue;
        }

        displayStatsGraph(stats, 'points');
        displayStatsGraph(stats, 'assists');
        displayStatsGraph(stats, 'rebounds');

        readline.question('\nPress Enter to search for another player...');
    }
}

// Start the application
main().catch(console.error);
