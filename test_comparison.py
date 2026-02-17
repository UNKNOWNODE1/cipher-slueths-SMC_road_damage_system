from decimal import Decimal

# Test Decimal vs Float comparison
d = Decimal('0.85')
f = 0.8
try:
    print(f"Greater: {d > f}")
except Exception as e:
    print(f"Comparison error: {e}")
