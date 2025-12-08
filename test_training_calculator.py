"""Test Training Calculator formulas."""

from pages.Training_Calculator import calculate_training_time, format_time_readable

# Test case 1: Skill 50 at 60% - time to reach skill 51
print("=" * 60)
print("Test 1: Knight Melee - Skill 50 at 60%, training to 51")
print("=" * 60)
result1 = calculate_training_time(50, 60, "Knight", "Melee")
print(f"Time: {format_time_readable(result1)}")
print(f"Current: Skill {result1['current_skill']} at {result1['current_percent']}%")
print(f"Target: Skill {result1['next_skill']}")
print(f"Remaining: {result1['remaining_percent']}%")
print(f"Seconds: {result1['seconds']}")
print(f"Minutes: {result1['minutes']}")
print(f"Hours: {result1['hours']}")
print()

# Test case 2: Skill 70 at 0% - time to reach skill 71 (full level)
print("=" * 60)
print("Test 2: Knight Melee - Skill 70 at 0%, training to 71 (full level)")
print("=" * 60)
result2 = calculate_training_time(70, 0, "Knight", "Melee")
print(f"Time: {format_time_readable(result2)}")
print(f"Current: Skill {result2['current_skill']} at {result2['current_percent']}%")
print(f"Target: Skill {result2['next_skill']}")
print(f"Remaining: {result2['remaining_percent']}%")
print(f"Seconds: {result2['seconds']}")
print(f"Minutes: {result2['minutes']}")
print(f"Hours: {result2['hours']}")
print(f"Days: {result2['days']}")
print()

# Test case 3: Skill 30 at 40% - time to reach skill 31
print("=" * 60)
print("Test 3: Knight Melee - Skill 30 at 40%, training to 31")
print("=" * 60)
result3 = calculate_training_time(30, 40, "Knight", "Melee")
print(f"Time: {format_time_readable(result3)}")
print(f"Current: Skill {result3['current_skill']} at {result3['current_percent']}%")
print(f"Target: Skill {result3['next_skill']}")
print(f"Remaining: {result3['remaining_percent']}%")
print(f"Seconds: {result3['seconds']}")
print(f"Minutes: {result3['minutes']}")
print(f"Hours: {result3['hours']}")
print()

# Test case 4: Skill 100 at 50% - time to reach skill 101
print("=" * 60)
print("Test 4: Knight Melee - Skill 100 at 50%, training to 101")
print("=" * 60)
result4 = calculate_training_time(100, 50, "Knight", "Melee")
print(f"Time: {format_time_readable(result4)}")
print(f"Current: Skill {result4['current_skill']} at {result4['current_percent']}%")
print(f"Target: Skill {result4['next_skill']}")
print(f"Remaining: {result4['remaining_percent']}%")
print(f"Seconds: {result4['seconds']}")
print(f"Minutes: {result4['minutes']}")
print(f"Hours: {result4['hours']}")
print(f"Days: {result4['days']}")
print()

# Manual verification for skill 50 at 60% (40% remaining)
print("=" * 60)
print("Manual calculation verification (Skill 50 at 60%, 40% remaining):")
print("=" * 60)
import math
base = 50
difficulty = math.pow(1.1, 50 - 10)
remaining = 100 - 60
percent = remaining / 100
manual_result = base * difficulty * percent
print(f"Formula: 50 × 1.1^(50-10) × ((100-60)/100)")
print(f"        = 50 × 1.1^40 × 0.40")
print(f"        = 50 × {difficulty:.4f} × 0.40")
print(f"        = {manual_result:.2f} seconds")
print(f"Calculator result: {result1['seconds']} seconds")
print(f"Match: {'✓ YES' if abs(manual_result - result1['seconds']) < 0.01 else '✗ NO'}")

