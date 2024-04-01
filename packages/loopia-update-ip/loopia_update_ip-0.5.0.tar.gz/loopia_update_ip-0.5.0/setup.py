import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loopia_update_ip",
    version="0.5.0",
    author="Niklas Melin",
    author_email="niklasme@pm.me",
    description="Application to keep DNS records updated when external "
                "IP-address change using the Loopia-API for the domain provider Loopia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/loopia-update-ip",
    packages=setuptools.find_packages(),
    install_requires=['setuptools',
                      'wheel',
                      'confuse',
                      'tldextract'
                      ],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'loopia-update-ip=loopia_update_ip.loopia_update_ip:update',
            'loopia-update-ip-service=loopia_update_ip.loopia_update_ip:service',
        ],
    },
)
