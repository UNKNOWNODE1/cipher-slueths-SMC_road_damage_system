import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smc_platform.settings')
django.setup()

from reports.models import Report

# Create a dummy report
r = Report(title="Test", ai_confidence=Decimal('0.8567'))
print(f"Confidence: {r.ai_confidence}")
try:
    print(f"Percent: {r.ai_confidence_percent}")
except Exception as e:
    print(f"Error: {e}")

r_none = Report(title="Test None", ai_confidence=None)
print(f"Confidence None: {r_none.ai_confidence}")
try:
    print(f"Percent None: {r_none.ai_confidence_percent}")
except Exception as e:
    print(f"Error None: {e}")
