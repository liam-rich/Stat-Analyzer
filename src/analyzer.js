import readline from 'readline-sync';
import { searchPlayer, getPlayerStats } from './api.js';
import { displayPlayerInfo } from './utils.js';

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
                limitMessage: 'Invalid choice.',
                limit: input => input > 0 && input <= players.length,
            });
            selectedPlayer = players[choice - 1];
        } else {
            selectedPlayer = players[0];
        }

        console.log(`\nFetching stats for ${selectedPlayer.name}...`);
        const stats = await getPlayerStats(selectedPlayer.id);

        if (!stats) {
            console.log('No stats available.');
            readline.question('Press Enter to try again...');
            continue;
        }

        displayPlayerInfo(stats);
        readline.question('\nPress Enter to search for another player...');
    }
}

main().catch(console.error);
