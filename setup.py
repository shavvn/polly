from setuptools import setup

setup(name="polly",
      version="0.1",
      description="Polly is a data visualization lib built on top of Matplotlib",
      url="https://github.com/shavvn/polly",
      author="Shang Li",
      author_email="shangli@umd.edu",
      packages=["polly"],
      install_requires= [
        "numpy",
        "matplotlib",
      ],
      classifiers=[
        "Development Status :: 0 dev release",
        "Programming Language :: Python :: 2.7",
        "Topic:: Data visualization"
      ],
      keywords="Data visualization, matplotlib"
      )
