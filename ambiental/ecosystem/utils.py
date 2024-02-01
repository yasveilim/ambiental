import random


def generate_reset_code():
    six_digits = random.randint(100000, 999999)
    return six_digits


def main():
    random_number = generate_reset_code()
    print("Your random number is: {}".format(random_number))


if __name__ == '__main__':
    main()
