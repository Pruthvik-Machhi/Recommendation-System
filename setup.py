from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    Reads the requirements.txt file and returns a list of packages, excluding '-e .' line.
    """
    requirement_list: List[str] = []
    try:
        with open("requirements.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(("#", "-e")):
                    requirement_list.append(line)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    
    return requirement_list

setup(
    name="Recommendation-System",
    version="0.0.1",
    author="Pruthvik-Machhi",
    packages=find_packages(),
    install_requires=get_requirements()
)