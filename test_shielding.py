"""Test Training Calculator for Shielding skill (Knight and Paladin)."""

from pages.Training_Calculator import calculate_training_time, format_time_readable
import math

print("=" * 70)
print("SHIELDING SKILL TESTS")
print("=" * 70)
print()

# Test Knight Shielding
print("KNIGHT SHIELDING")
print("-" * 70)
print()

# Test case 1: Knight Shielding - Skill 50 at 0% (full level)
print("Test 1: Knight Shielding - Skill 50 at 0%, training to 51 (full level)")
result1 = calculate_training_time(50, 0, "Knight", "Shielding")
print(f"Time: {format_time_readable(result1)}")
print(f"Current: Skill {result1['current_skill']} at {result1['current_percent']}%")
print(f"Target: Skill {result1['next_skill']}")
print(f"Seconds: {result1['seconds']}")
print(f"Minutes: {result1['minutes']}")
print(f"Hours: {result1['hours']}")
print()

# Manual calculation for Knight Shielding skill 50
print("Manual calculation (Knight Shielding - Skill 50):")
delta = 50
factor = 1000 / 1100
hits_needed = delta * math.pow(factor, 50 - 10)
time_minutes = (hits_needed * 2) / 60
time_seconds = time_minutes * 60
print(f"Formula: HitsNeeded = 50 × (1000/1100)^(50-10)")
print(f"        = 50 × (0.9091)^40")
print(f"        = 50 × {math.pow(factor, 40):.6f}")
print(f"        = {hits_needed:.2f} hits")
print(f"TimeMinutes = ({hits_needed:.2f} × 2) / 60")
print(f"           = {time_minutes:.2f} minutes")
print(f"           = {time_seconds:.2f} seconds")
print(f"Calculator result: {result1['seconds']} seconds")
print(f"Match: {'✓ YES' if abs(time_seconds - result1['seconds']) < 0.1 else '✗ NO'}")
print()

# Test case 2: Knight Shielding - Skill 70 at 50%
print("Test 2: Knight Shielding - Skill 70 at 50%, training to 71")
result2 = calculate_training_time(70, 50, "Knight", "Shielding")
print(f"Time: {format_time_readable(result2)}")
print(f"Seconds: {result2['seconds']}, Minutes: {result2['minutes']}, Hours: {result2['hours']:.2f}")
print()

print("=" * 70)
print("PALADIN SHIELDING")
print("-" * 70)
print()

# Test case 3: Paladin Shielding - Skill 50 at 0% (full level)
print("Test 3: Paladin Shielding - Skill 50 at 0%, training to 51 (full level)")
result3 = calculate_training_time(50, 0, "Paladin", "Shielding")
print(f"Time: {format_time_readable(result3)}")
print(f"Current: Skill {result3['current_skill']} at {result3['current_percent']}%")
print(f"Target: Skill {result3['next_skill']}")
print(f"Seconds: {result3['seconds']}")
print(f"Minutes: {result3['minutes']}")
print(f"Hours: {result3['hours']}")
print()

# Manual calculation for Paladin Shielding skill 50
print("Manual calculation (Paladin Shielding - Skill 50):")
delta = 100
factor = 1100 / 1000
hits_needed = delta * math.pow(factor, 50 - 10)
time_minutes = (hits_needed * 2) / 60
time_seconds = time_minutes * 60
print(f"Formula: HitsNeeded = 100 × (1100/1000)^(50-10)")
print(f"        = 100 × (0.9091)^40")
print(f"        = 100 × {math.pow(factor, 40):.6f}")
print(f"        = {hits_needed:.2f} hits")
print(f"TimeMinutes = ({hits_needed:.2f} × 2) / 60")
print(f"           = {time_minutes:.2f} minutes")
print(f"           = {time_seconds:.2f} seconds")
print(f"Calculator result: {result3['seconds']} seconds")
print(f"Match: {'✓ YES' if abs(time_seconds - result3['seconds']) < 0.1 else '✗ NO'}")
print()

# Test case 4: Paladin Shielding - Skill 80 at 25%
print("Test 4: Paladin Shielding - Skill 80 at 25%, training to 81")
result4 = calculate_training_time(80, 25, "Paladin", "Shielding")
print(f"Time: {format_time_readable(result4)}")
print(f"Seconds: {result4['seconds']}, Minutes: {result4['minutes']}, Hours: {result4['hours']:.2f}")
print()

# Comparison
print("=" * 70)
print("COMPARISON: Knight vs Paladin Shielding (Skill 60, 0%)")
print("-" * 70)
knight_shield = calculate_training_time(60, 0, "Knight", "Shielding")
paladin_shield = calculate_training_time(60, 0, "Paladin", "Shielding")

print(f"Knight Shielding:  {format_time_readable(knight_shield)}")
print(f"                   {knight_shield['minutes']:.2f} minutes")
print()
print(f"Paladin Shielding: {format_time_readable(paladin_shield)}")
print(f"                   {paladin_shield['minutes']:.2f} minutes")
print()
print(f"Paladin takes {paladin_shield['minutes'] / knight_shield['minutes']:.2f}x longer")
print(f"(Delta: Knight=50, Paladin=100)")
print()

# Multi-skill comparison for skill 50
print("=" * 70)
print("ALL SKILLS COMPARISON (Skill 50, full level)")
print("-" * 70)
knight_melee = calculate_training_time(50, 0, "Knight", "Melee")
knight_shield = calculate_training_time(50, 0, "Knight", "Shielding")
paladin_dist = calculate_training_time(50, 0, "Paladin", "Distance")
paladin_shield = calculate_training_time(50, 0, "Paladin", "Shielding")

print(f"Knight Melee:       {knight_melee['minutes']:6.2f} minutes ({knight_melee['hours']:.2f} hours)")
print(f"Knight Shielding:   {knight_shield['minutes']:6.2f} minutes ({knight_shield['hours']:.2f} hours)")
print(f"Paladin Distance:   {paladin_dist['minutes']:6.2f} minutes ({paladin_dist['hours']:.2f} hours)")
print(f"Paladin Shielding:  {paladin_shield['minutes']:6.2f} minutes ({paladin_shield['hours']:.2f} hours)")
print()
