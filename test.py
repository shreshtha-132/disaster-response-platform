import asyncio
import sys
import os

# Add root to sys.path to resolve "api" imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.geocode import getLocationAndCoordinates

description = "There is heavy flooding in Bandra, Mumbai near the railway station."

result = asyncio.run(getLocationAndCoordinates(description))
print(result)

