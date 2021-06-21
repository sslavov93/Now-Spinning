from setuptools import find_packages, setup

setup(
    name="now_spinning",
    description="",
    version="0.0.1",
    author="Svet",
    url="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["now_spinning"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask", "black", "flake8", "flask_sqlalchemy"
    ],
    # entry_points={"console_scripts": ["realpython=reader.__main__:main"]},
)
