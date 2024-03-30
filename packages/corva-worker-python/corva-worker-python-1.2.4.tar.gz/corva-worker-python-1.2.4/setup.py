from setuptools import find_packages, setup

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Software Development :: Libraries",
]

setup(
    name="corva-worker-python",
    author="Jordan Ambra <jordan.ambra@corva.ai>, Mohammadreza Kamyab <m.kamyab@corva.ai>",
    url="https://github.com/corva-ai/corva-worker-python",
    version="1.2.4",
    classifiers=classifiers,
    python_requires=">=3.8",
    description="SDK for interacting with Corva",
    keywords="corva, worker",
    packages=find_packages(exclude=["testcase"]),
    install_requires=["numpy", "redis", "requests", "simplejson"],
    include_package_data=True,
    license="Unlicensed",
)
