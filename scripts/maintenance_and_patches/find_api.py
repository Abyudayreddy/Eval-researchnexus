import os
for root, dirs, files in os.walk('c:/Users/Abyureddy/Downloads/SDC2/src'):
    if 'api.ts' in files:
        print(os.path.join(root, 'api.ts'))
