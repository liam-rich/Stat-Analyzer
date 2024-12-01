Testing Procedures
Manual Testing Checklist
Player Search

Launch application: node analyzer.js
Enter a player name

Expected: List of matching players should appear
Test with: "James", "Curry", "Giannis"
Test with partial names
Test with invalid names



Player Selection

When multiple players are found:

Verify numbered list appears
Test selecting valid numbers
Test selecting invalid numbers



Statistics Display

For each selected player:

Verify points graph appears
Verify assists graph appears
Verify rebounds graph appears
Check that averages are calculated correctly



Error Handling

Test network failures:

Disconnect internet
Verify appropriate error message


Test invalid inputs:

Empty player name
Special characters
Extremely long names



Automated Testing
Future development will include Jest-based unit tests for:

Player search functionality
Data processing
Graph generation
Average calculations
