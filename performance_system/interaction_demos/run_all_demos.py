#!/usr/bin/env python3
"""
Run All BrainJam MVP Demos

Executes the three required MVP demonstrations:
1. Brain → Continuous Sound
2. AI as Co-Performer
3. Learning Through Practice
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from demo1_continuous_sound import generate_continuous_texture
from demo2_ai_coperformer import generate_coperformance
from demo3_learning_practice import simulate_practice_session


def run_all_demos():
    """Run all three MVP demos in sequence."""
    
    print("\n" + "=" * 70)
    print("BrainJam MVP Demonstrations")
    print("=" * 70)
    print("\nThis script will run all three required demos:")
    print("  1. Brain → Continuous Sound (30s)")
    print("  2. AI as Co-Performer (40s)")
    print("  3. Learning Through Practice (60s)")
    print("\nTotal duration: ~130 seconds")
    print("=" * 70)
    
    input("\nPress Enter to start...\n")
    
    # Demo 1
    print("\n" + "▶" * 35)
    print("Starting Demo 1...")
    print("▶" * 35 + "\n")
    try:
        generate_continuous_texture(duration=30.0)
        print("\n✓ Demo 1 completed successfully!\n")
    except Exception as e:
        print(f"\n✗ Demo 1 failed: {e}\n")
    
    input("Press Enter to continue to Demo 2...\n")
    
    # Demo 2
    print("\n" + "▶" * 35)
    print("Starting Demo 2...")
    print("▶" * 35 + "\n")
    try:
        generate_coperformance(duration=40.0)
        print("\n✓ Demo 2 completed successfully!\n")
    except Exception as e:
        print(f"\n✗ Demo 2 failed: {e}\n")
    
    input("Press Enter to continue to Demo 3...\n")
    
    # Demo 3
    print("\n" + "▶" * 35)
    print("Starting Demo 3...")
    print("▶" * 35 + "\n")
    try:
        simulate_practice_session(duration=60.0)
        print("\n✓ Demo 3 completed successfully!\n")
    except Exception as e:
        print(f"\n✗ Demo 3 failed: {e}\n")
    
    # Summary
    print("\n" + "=" * 70)
    print("All Demos Complete!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  • demo1_continuous_texture.wav")
    print("  • demo2_ai_coperformer.wav")
    print("  • demo3_learning_practice.wav")
    print("  • demo3_learning_curve.png")
    print("\nThese demos show:")
    print("  ✓ Real-time brain → sound pipeline")
    print("  ✓ AI as responsive co-performer")
    print("  ✓ Learning and stabilization over practice")
    print("  ✓ Low-latency performance capability")
    print("=" * 70)


if __name__ == "__main__":
    run_all_demos()
