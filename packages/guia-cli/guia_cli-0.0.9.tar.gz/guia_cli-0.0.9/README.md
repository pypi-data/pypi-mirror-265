
[![Publish to PyPI](https://github.com/andersonbosa/guia-cli/actions/workflows/publish.yml/badge.svg)](https://pypi.org/project/guia-cli/)
[![Creative Commons](https://img.shields.io/badge/license-CC0%201.0-white.svg?style=flat)](http://creativecommons.org/publicdomain/zero/1.0/)
[![https://img.shields.io/badge/made%20with-AI-blue](https://img.shields.io/badge/made%20with-AI-blue)](#)


---
<section align="center">
  <img src="docs/assets/images/banner.svg" title="Project banner" alt="Project banner" />
  <br>
  <br>

  <p>
    <a href="#about">About</a> •
    <a href="#installation">Installation</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#contribution">Contribution</a> •
    <a href="#license">License</a>
  </p>
</section>

---

## About

Gu IA Agent (aka GuIA-CLI) is an agent specializing in software engineering, designed to assist in programming tasks and provide technical guidance.It is able to generate code based on provided requirements and answer technical questions, offering clear explanations and relevant recommendations.

## Installation

You can install Guia-CLI via PyPI using pip:

```bash
pip install guia-cli
```

Alternatively, you can build from the repository:

1. Clone the repository:
```bash
git clone https://github.com/andersonbosa/guia-cli.git
```

2. Navigate to the repository directory:
```bash
cd repo
```

3. Install the package:
```bash
python setup.py install
```


## Getting Started

To use the GU agent, you can execute the script `main.py` providing the following options:

- `--coding "YOUR REQUEST"`: Uses Gu agent programming ability to generate code based on your request.
- `--mentoring "YOUR QUESTION"`: Uses Gu agent mentoring ability to receive technical guidance in response to your question.

#### Settings

Be sure to configure the following environment variables or it is setup in the `.env` file:

- `GOOGLE_API_KEY`: Your Google API key to use Gemini service (required)

#### Example of use

```bash
python main.py --coding "Implement a function to order a Python list using bubble-sort"
```

```bash
python main.py --mentoring "What is the difference between inheritance and composition in object -oriented programming?"
```

#### Backup results

The results of interactions with agent GU are saved in the `outputs` folder. Each file generated contains the date, type of interaction and a description of the request.


## 🤝 Contribution

<p>
  This project is for study purposes too, so please send me a message telling me what you are doing and why you are doing it, teach me what you know. All kinds of contributions are very welcome and appreciated!
</p>


## 📝 License

This project is under the [public domain](LICENSE.md) license.

---

<h4>  
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/andersonbosa/guia-cli?style=social">
  | Did you like the repository? Give it a star! 😁
</h4>

