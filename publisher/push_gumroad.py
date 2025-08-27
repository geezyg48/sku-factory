import os, sys
if not os.environ.get('GUMROAD_TOKEN'):
    print('Gumroad token not set. Skipping upload (safe no-op).'); sys.exit(0)
print('Simulated Gumroad publish (extend with real API calls).')
