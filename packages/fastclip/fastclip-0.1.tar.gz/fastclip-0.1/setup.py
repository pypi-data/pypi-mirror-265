from distutils.core import setup

setup(
    name="fastclip",
    packages=["fastclip"],
    version="0.1",
    license="MIT",
    description="A private library for fastclip",
    author="Fastclip",
    author_email="hello+pip@fastclip.io",
    url="https://github.com/fastclip/library",
    download_url="https://github.com/fastclip/library/archive/v_01.tar.gz",
    keywords=[
        "fastclip",
    ],
    install_requires=[
        "typing_extensions",
        "pydantic",
    ],
)
