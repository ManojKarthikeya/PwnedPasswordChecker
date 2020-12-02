import requests
import hashlib
import sys


def get_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    api_data = requests.get(url)
    if api_data.status_code != 200:
        raise RuntimeError(f'Error Fetching: {api_data.status_code}')
    return api_data


def check_password(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_five = sha1_password[:5]
    remaining = sha1_password[5:]
    response = get_api_data(first_five)
    return count_password_pwns(response, remaining)


def count_password_pwns(hashes, hash_to_check):
    hash_list = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hash_list:
        if h == hash_to_check:
            return count
    return 0


def main(args):
    for item in args:
        count = check_password(item)
        if count:
            print(f'{item} has been found {count} times. Consider changing your password')
        else:
            print(f'{item} was not found! Your password is secure')


if __name__ == '__main__':
    main(sys.argv[1:])
