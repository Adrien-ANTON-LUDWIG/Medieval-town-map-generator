"""This modules generates medieval towns' maps."""
from src.city import City
import src.tools as tools
import subprocess


def main():
    city = City(5000)
    tools.json(city, './resources/city.json')
    subprocess.call('python3 src/viewer.py resources/city.json', shell=True)


if __name__ == '__main__':
    main()
