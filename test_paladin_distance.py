"""Test Training Calculator for Paladin Distance skill."""

from pages.Training_Calculator import calculate_training_time, format_time_readable
import math

print("=" * 70)
print("PALADIN DISTANCE SKILL TESTS")
print("=" * 70)
print()

# Test case 1: Paladin Distance - Skill 50 at 0% (full level)
print("Test 1: Paladin Distance - Skill 50 at 0%, training to 51 (full level)")
print("-" * 70)
result1 = calculate_training_time(50, 0, "Paladin", "Distance")
print(f"Time: {format_time_readable(result1)}")
print(f"Current: Skill {result1['current_skill']} at {result1['current_percent']}%")
print(f"Target: Skill {result1['next_skill']}")
print(f"Remaining: {result1['remaining_percent']}%")
print(f"Seconds: {result1['seconds']}")
print(f"Minutes: {result1['minutes']}")
print(f"Hours: {result1['hours']}")
print()

# Manual calculation for skill 50
print("Manual calculation (Skill 50, 0% to 100%):")
delta = 30
factor = 1100 / 1000
hits_needed = delta * math.pow(factor, 50 - 10)
time_minutes = (hits_needed * 2) / 60
time_seconds = time_minutes * 60
print(f"Formula: HitsNeeded = 30 × (1.1)^(50-10)")
print(f"        = 30 × (1.1)^40")
print(f"        = 30 × {math.pow(1.1, 40):.4f}")
print(f"        = {hits_needed:.2f} hits")
print(f"TimeMinutes = ({hits_needed:.2f} × 2) / 60")
print(f"           = {time_minutes:.2f} minutes")
print(f"           = {time_seconds:.2f} seconds")
print(f"Calculator result: {result1['seconds']} seconds")
print(f"Match: {'✓ YES' if abs(time_seconds - result1['seconds']) < 0.1 else '✗ NO'}")
print()

# Test case 2: Paladin Distance - Skill 70 at 50%
print("=" * 70)
print("Test 2: Paladin Distance - Skill 70 at 50%, training to 71")
print("-" * 70)
result2 = calculate_training_time(70, 50, "Paladin", "Distance")
print(f"Time: {format_time_readable(result2)}")
print(f"Current: Skill {result2['current_skill']} at {result2['current_percent']}%")
print(f"Target: Skill {result2['next_skill']}")
print(f"Remaining: {result2['remaining_percent']}%")
print(f"Seconds: {result2['seconds']}")
print(f"Minutes: {result2['minutes']}")
print(f"Hours: {result2['hours']}")
print()

# Test case 3: Paladin Distance - Skill 80 at 25%
print("=" * 70)
print("Test 3: Paladin Distance - Skill 80 at 25%, training to 81")
print("-" * 70)
result3 = calculate_training_time(80, 25, "Paladin", "Distance")
print(f"Time: {format_time_readable(result3)}")
print(f"Current: Skill {result3['current_skill']} at {result3['current_percent']}%")
print(f"Target: Skill {result3['next_skill']}")
print(f"Remaining: {result3['remaining_percent']}%")
print(f"Seconds: {result3['seconds']}")
print(f"Minutes: {result3['minutes']}")
print(f"Hours: {result3['hours']}")
print(f"Days: {result3['days']}")
print()

# Compare Knight vs Paladin for same skill level
print("=" * 70)
print("COMPARISON: Knight Melee vs Paladin Distance (Skill 60, 0%)")
print("-" * 70)
knight_result = calculate_training_time(60, 0, "Knight", "Melee")
paladin_result = calculate_training_time(60, 0, "Paladin", "Distance")

print(f"Knight Melee:    {format_time_readable(knight_result)}")
print(f"                 {knight_result['hours']} hours")
print()
print(f"Paladin Distance: {format_time_readable(paladin_result)}")
print(f"                 {paladin_result['hours']} hours")
print()
print(f"Difference: {abs(knight_result['hours'] - paladin_result['hours']):.2f} hours")
print()
