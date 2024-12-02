/**
 * Display player information
 * @param {Object} stats - Player stats and details
 */
export function displayPlayerInfo(stats) {
    console.log('\nPlayer Information:');
    console.log(`Name: ${stats.name}`);
    console.log(`Team: ${stats.team}`);
    console.log(`Position: ${stats.position}`);
    console.log(`Birth Date: ${stats.birthDate}`);
    console.log(`Description: ${stats.description}`);
}
