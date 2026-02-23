with open('Track/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f'Total lines: {len(lines)}')
    print('Line 1580-1590:')
    for i in range(1579, min(1590, len(lines))):
        print(f'{i+1}: {lines[i]}', end='')
