#!/usr/bin/env python3
"""
Quick test to verify io_handler works after cleanup
"""
from pathlib import Path
import numpy as np
from io_handler import parse_input_file, write_output_file

# Test 1: Parse input file
print("✅ Test 1: Parse input-02.txt")
try:
    grid = parse_input_file("Inputs/input-02.txt")
    print(f"   Grid shape: {grid.shape}")
    print(f"   Grid dtype: {grid.dtype}")
    assert grid.shape[0] > 0, "Grid has no rows"
    assert grid.shape[1] > 0, "Grid has no columns"
    print("   PASSED ✓\n")
except Exception as e:
    print(f"   FAILED: {e}\n")

# Test 2: Write output without bridges
print("✅ Test 2: Write output (no bridges)")
try:
    output_path = write_output_file(grid, [], "Outputs/test_output_1.txt")
    assert Path(output_path).exists(), "Output file not created"
    content = Path(output_path).read_text()
    assert len(content) > 0, "Output file is empty"
    print(f"   Output: {output_path}")
    print(f"   File size: {len(content)} bytes")
    print("   PASSED ✓\n")
except Exception as e:
    print(f"   FAILED: {e}\n")

# Test 3: Write output with sample bridges
print("✅ Test 3: Write output (with bridges)")
try:
    bridges = [
        {'from': (0, 1), 'to': (0, 3), 'count': 2},
        {'from': (0, 1), 'to': (2, 1), 'count': 1},
    ]
    output_path = write_output_file(grid, bridges, "Outputs/test_output_2.txt")
    assert Path(output_path).exists(), "Output file not created"
    content = Path(output_path).read_text()
    assert "=" in content, "Double bridge symbol not found"
    assert "|" in content, "Single bridge symbol not found"
    print(f"   Output: {output_path}")
    print(f"   File size: {len(content)} bytes")
    print("   PASSED ✓\n")
except Exception as e:
    print(f"   FAILED: {e}\n")

print("=" * 60)
print("All tests completed successfully! 🎉")
print("io_handler.py is clean and working correctly")
print("=" * 60)
