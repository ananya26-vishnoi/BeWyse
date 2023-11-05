# Installation

```bash
git clone https://github.com/<your username>/<Project Name>.git
```

If you haven't verified your Git account, don't worry! You can still download the project as a zip file and extract it to your local machine. This option is provided at the last step of project creation, so you can easily access and work with the files even without a Git account.

# Prerequisites

Before you start using this project, make sure you have the following set up:

 - Python installed on your system.
 - Django and Django REST framework installed.
 - Firebase Admin SDK for token verification.
 - MongoDB server running locally or accessible via the specified connection URL.
 
# Setup

## Virtual Environment


To ensure a clean and organized development environment, it is highly recommended to use a virtual environment when working with any project. You can create a virtual environment for your project by running the following command in your terminal:

```bash
python -m venv <name of virtual environment>
```

Once your virtual environment is created, you can activate it using the appropriate command for your operating system.

Windows:
```bash
.\<name of virtual environment>\Scripts\activate
```

Linux/Unix:
```bash
source <name of virtual environment>/bin/activate
```

By activating your virtual environment, you can ensure that any dependencies and packages you install will be isolated from your global environment, making it easier to manage and maintain your project.

## Installing Dependencies


      
To install all the necessary dependencies for your project, simply run the following command in your terminal:

```bash
pip install -r requirements.txt
```
This command will read the requirements.txt file and automatically install all the listed dependencies for you. Make sure your virtual environment is activated before running this command to ensure that the packages are installed in the correct environment. Once the installation is complete, you'll be ready to start working on your project!

## .env



<b> Important Note: </b>
Please ensure that you add all the necessary sensitive information, such as database credentials and API keys, to the .env file. This file is used to store this information securely and is not pushed to GitHub by default. However, please note that we have added the .env file to the repository, but it is empty to ensure that you can fill it out with the required data.

To prevent any accidental disclosure of sensitive information, make sure to add the .env file to the .gitignore file before committing your code to the repository. This way, you can keep your data secure while still being able to utilize the benefits of version control.
