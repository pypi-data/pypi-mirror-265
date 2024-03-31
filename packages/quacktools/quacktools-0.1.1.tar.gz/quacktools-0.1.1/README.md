# quacktools-codeforces
Quacktools streamlines the code testing and code submission process for Codeforces users.

### Built with

[Python.io]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python.io"/>
</p>


## Getting Started

To guarantee a seamless experience moving forward, please read and follow the installation instructions carefully.

### Installation

To install `quacktools`, use the `pip` command below:
   ```sh
   pip install quacktools
   ```

To clone and work on the project, simply follow the instructions as listed below:

1. Clone the repository
   ```sh
   git https://github.com/DuckyShine004/quacktools-codeforces.git
   ```
2. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```
### Usage
```
usage: quack [-h] [-t FILE] [-p PROBLEM] [-c CONTEST] [-d DIFFICULTY]

options:
  -h, --help     show this help message and exit
  -t FILE        Test your file against a problem from a problem set, or a
                 problem from a contest.
  -p PROBLEM     What is the problem number, e.g. 1950.
  -c CONTEST     What is the contest number, e.g. 1950.
  -d DIFFICULTY
```
#### Detailed Usage

To use `quacktools`, you must use the `quack` command. See below for detailed usage:
1. Using `quacktools` to test your code for any problem from the problemset section:
   ```sh
   quack -t <file> -p <problemset-problem-number> -d <problem-difficulty>
   ```
2. Using `quacktools` to test your code for any problem from a contest:
   ```sh
   quack -t <file> -p <contest-problem-number> -d <problem-difficulty>
   ```

**NOTE:** Your `file` must reside in the same directory from which you are invoking the `quack` command.

## Contribution

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. Don't forget to give the project a star! (⭐)

1. Fork the Project
2. Create your Feature Branch (`git checkout -b Feat/NewFeature`)
3. Commit your Changes (`git commit -m 'Feat: Added New Feature'`)
4. Push to the Branch (`git push origin Feat/NewFeature`)
5. Open a Pull Request

## License

Distributed under the `MIT License`. See `LICENSE.txt` for more information.

## Contact

Gallon Zhou: [Linkedin](https://www.linkedin.com/in/gallon-zhou-a3739b278/)

Project Link: [https://github.com/DuckyShine004/quacktools-codeforces](https://github.com/DuckyShine004/quacktools-codeforces)
