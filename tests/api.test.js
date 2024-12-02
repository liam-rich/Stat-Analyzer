import { searchPlayer, getPlayerStats } from '../src/api.js';

test('searchPlayer returns player data', async () => {
    const players = await searchPlayer('LeBron James');
    expect(players.length).toBeGreaterThan(0);
    expect(players[0]).toHaveProperty('id');
    expect(players[0]).toHaveProperty('name');
});

test('getPlayerStats returns stats data', async () => {
    const stats = await getPlayerStats(237); // LeBron James ID
    expect(stats.length).toBeGreaterThan(0);
    expect(stats[0]).toHaveProperty('points');
});
