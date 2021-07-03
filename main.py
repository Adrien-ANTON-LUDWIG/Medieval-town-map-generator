"""This modules generates medieval towns' maps."""
from src.city import City
import src.tools as tools


def main():
    city = City(5000)
    tools.json(city, './resources/city.json')


if __name__ == '__main__':
    main()
