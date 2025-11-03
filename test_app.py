print('Testing app.py...')

# Read the app.py file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if the launch line exists
if 'demo.launch' in content:
    print('✓ Launch command found')
    # Find and print the launch line
    for line in content.split('\n'):
        if 'demo.launch' in line:
            print(f'Launch line: {line.strip()}')
else:
    print('✗ No launch command found!')

# Check if it's inside if __name__ == '__main__'
if '__name__' in content:
    print('✓ Main block found')
else:
    print('✗ No main block found!')

print('\nNow trying to run app.py...')
exec(content)
