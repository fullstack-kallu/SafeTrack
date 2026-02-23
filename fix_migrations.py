#!/usr/bin/env python
import sys

# Read the migration file
with open('Track/migrations/0001_initial.py', 'r') as f:
    content = f.read()

# Replace all managed: False with managed: True
content = content.replace("'managed': False,", "'managed': True,")

# Write back
with open('Track/migrations/0001_initial.py', 'w') as f:
    f.write(content)

print("Updated migration file - all 'managed': False changed to 'managed': True")
