
def print_menu(options: list, sep=None, title='Menu', input_text='Select an option: ') -> str:
    """
    Parameters
    ----------
    title: Title to print before the options (default='Menu')
    bar: Separator to print between title and the options
    options: List of string to print
    input_text: Text to print after options (default='Select an option:')

    Returns
    -------
    Number of option selected starting from 1 (String)

    """
    print(f'{title}:')
    if sep:
        print(sep)
    for indx, o in enumerate(options):
        print(f'[{indx + 1}] {o}')
    print(f'[{len(options)+1}] Exit')
    try:
        choice = input(f'{input_text}')
        while choice not in str(range(1, len(options) + 1)):
            choice = input('Select a valid option: ')
    except KeyboardInterrupt:
        return len(options) + 1

    return choice
