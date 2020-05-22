try:
    f = open('source.txt')
    if not f.name == 'source.txt':
        raise Exception
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print('Error!')
else:
    print(f.read())
    f.close()
finally:
    print("Executing finally...")