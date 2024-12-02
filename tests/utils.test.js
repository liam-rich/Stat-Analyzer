import { displayStatsGraph } from '../src/utils.js';

test('displayStatsGraph does not throw errors', () => {
    const stats = [
        { points: 25, assists: 5, rebounds: 10 },
        { points: 20, assists: 7, rebounds: 8 },
    ];
    expect(() => displayStatsGraph(stats, 'points')).not.toThrow();
});
