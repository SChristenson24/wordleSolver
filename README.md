# CLI AI Wordle Solver
### Wordle Overview

**Wordle** is an online word game that become popular within the recent years. It consists of a 6 x 5 grid, a keyboard, and a hidden random target word that changes everyday. Users are expected to input a 5-word guess (that is within the Wordle dictionary) and the game will give them letter-by-letter feedback as follows:

**Green** means the guessed letter is within the target word and is within the correct poisition.

**Yellow** means the guessed letter is within the target word, but is within the incorrect position.

**Grey** means the guessed letter is not within the target word.

Users win by guessing the target word within 6 attempts. **Wordle can be played here:** [New York Times Wordle](https://www.nytimes.com/games/wordle/index.html)
 
Here is example gameplay:


<img src="https://github.com/SChristenson24/wordleSolver/assets/124697781/5ed6f369-2f0c-43f5-9588-1b8e24cd6144" width="200" height="250"/>




### Detailed Instructions

## 1. Downloading Application
There are a couple of ways to download this application:
### Using GitHub Desktop
- Make sure to have GitHub Desktop and Visual Studio Code installed on your machine
- Navigate to the green "<> Code" dropdown menu within this repository.
- Click "Open with GitHub Desktop", which will take you to GitHub Desktop
- Set the local path to where you want the application
- Then click "Open with Visual Studio Code'

### Using Git Commands
- Navigate to your terminal
- Navigate to where you wish to clone the repository to
  ```
  cd /your/file/path/to/code/here
  ```
- Once you are in the file location you'd like the to clone to, use this command
  ```
  git clone https://github.com/SChristenson24/wordleSolver.git
  ```
## 2. Running the application
### Python Installation
**you must have python installed** to run this application.

To check if you have Python installed, run the version command:
```
python --version
```
or
```
python3 --version
```
If you do no get an output with the python version, you will need to install python and pip.

### File Execution
Run this command (in your choice of editor terminal):
```
python wordleSolve.py
```
or
```
python3 wordleSolve.py
```
## 3. How To Use 
While using this application, you will also need to be playing a game of Wordle on either:
[New York Times Wordle](https://www.nytimes.com/games/wordle/index.html)
or
[Wordle Unlimited](https://wordleunlimited.org/).

When you run the application, you will first be prompted with: 
```
Enter correct letters with their positions (e.g., 1a 3c), or type 'solved' to end:
```
This is asking for the **green letters** and their positions within your Wordle guess. For example:
<img width="343" alt="Screenshot 2024-03-11 at 12 59 46 PM" src="https://github.com/SChristenson24/wordleSolver/assets/124697781/736f186f-4801-4d30-8658-5423a41b2bc7">

You would input ``` 2r ```.

Once that is inputted, you will be prompted with:
```
Enter letters known to be in the word with wrong positions (e.g., 1r for 'r' not in position 1):
```
This is asking for the **yellow letters** and their positions within your Wordle guess. For this same example:
<img width="343" alt="Screenshot 2024-03-11 at 12 59 46 PM" src="https://github.com/SChristenson24/wordleSolver/assets/124697781/736f186f-4801-4d30-8658-5423a41b2bc7">

Your would input ``` 1g ```.

Once that is inputted, you will be prompted with:
```
Enter letters known not to be in the word:
```
This is asking for the **gray letters** and their positions within your Wordle guess. For this same example:
<img width="343" alt="Screenshot 2024-03-11 at 12 59 46 PM" src="https://github.com/SChristenson24/wordleSolver/assets/124697781/736f186f-4801-4d30-8658-5423a41b2bc7">


Your input would be ```ape```.

After inputting all of the letters from your wordle guess, you will be given a list of possible words. Use one of those words to input within your game. You will either input **y** (yes) or **n** (no) depending on if the word you chose solved the Wordle. 


### Technical Overview

This application was built to learn more in-depth about AI for course CSE 4633: Artificial Intelligence at Mississippi State University. 

We utilized both Breadth-First Search (BFS) and a Trie data structure
