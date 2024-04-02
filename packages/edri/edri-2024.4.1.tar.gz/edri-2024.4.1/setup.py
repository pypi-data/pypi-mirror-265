from setuptools import setup, find_packages

long_description = """**EDRI (Event Driven Routing Infrastructure)** is a project aimed at enhancing application development by utilizing 
parallelism—executing code across multiple threads, processes, or even different machines. It adopts an **event-driven** strategy, 
where events act as messages exchanged between various components to control and manage operations. Drawing parallels with TCP/IP in 
computer networks, EDRI's **routing infrastructure** facilitates the exchange and delivery of events. Instead of IP ranges, event types (
e.g., file uploads) are used to determine the destination of each event, ensuring efficient and targeted delivery to the appropriate 
recipients. This approach streamlines the process of managing distributed tasks within applications."""

setup(
    name='edri',
    version='2024.04.01',
    packages=find_packages(),
    description='Event Driven Routing Infrastructure',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Marek Olšan',
    author_email='marek.olsan@gmail.com',
    install_requires=[
        "typeguard>=4.0",
        "websockets>=12.0",
        "requests>=2.0",
        "validators>=0.22.0",
        "uvicorn>=0.27.0",
        "typing_extensions>=4.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Natural Language :: Czech",
        "Typing :: Typed"
    ],
)
