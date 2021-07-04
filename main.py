"""This modules generates medieval towns' maps."""

from src.town_generator import tools
from src.town_generator import viewer
from src.town_generator.city import City
import sys


def main(citizens=5000):
    city = City(citizens)
    tools.json(city, './resources/city.json')
    viewer.display('./resources/city.json')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        main()
    main(int(sys.argv[1]))
