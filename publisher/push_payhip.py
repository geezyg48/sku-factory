import os, sys
if not os.environ.get('PAYHIP_TOKEN'):
    print('Payhip token not set. Skipping upload (safe no-op).'); sys.exit(0)
print('Simulated Payhip publish (extend with real API calls).')
