import fetch from 'node-fetch';

const API_BASE = 'https://www.thesportsdb.com/api/v1/json/1';

/**
 * Search for a player by name
 * @param {string} playerName - Name of the player
 * @returns {Promise<Array>} - List of players
 */
export async function searchPlayer(playerName) {
    try {
        const response = await fetch(`${API_BASE}/searchplayers.php?p=${playerName}`);
        const data = await response.json();

        if (!data.player || data.player.length === 0) {
            throw new Error('No players found');
        }

        return data.player.map(player => ({
            id: player.idPlayer,
            name: `${player.strPlayer}`,
            team: player.strTeam || 'No Team',
        }));
    } catch (error) {
        console.error('Error searching for player:', error);
        return [];
    }
}

/**
 * Get statistics for a specific player
 * @param {string} playerId - Player's ID
 * @returns {Promise<Object>} - Player details and basic stats
 */
export async function getPlayerStats(playerId) {
    try {
        const response = await fetch(`${API_BASE}/lookupplayer.php?id=${playerId}`);
        const data = await response.json();

        if (!data.players || data.players.length === 0) {
            throw new Error('No stats found');
        }

        const player = data.players[0];
        return {
            name: player.strPlayer,
            team: player.strTeam,
            position: player.strPosition,
            description: player.strDescriptionEN || 'No description available.',
            birthDate: player.dateBorn || 'Unknown',
        };
    } catch (error) {
        console.error('Error fetching player stats:', error);
        return null;
    }
}
