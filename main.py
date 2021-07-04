"""This modules generates medieval towns' maps."""
from src.town_generator import tools
from src.town_generator import viewer
from src.town_generator.city import City


def main():
    city = City(5000)
    tools.json(city, './resources/city.json')
    viewer.displays('./resources/city.json')


if __name__ == '__main__':
    main()
