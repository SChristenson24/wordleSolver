function startGame() {
    fetch('/start_game')
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Error starting game:', error));
}

function startNewGame() {
    fetch('/start_game', {
        method: 'GET' 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to start a new game');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message); 
        resetBoard(); 
    })
    .catch(error => {
        console.error('Error starting new game:', error);
    });
}

function resetBoard() {
    document.querySelectorAll('.wordleRow .wordleCell').forEach(cell => {
        cell.value = '';
        cell.style.backgroundColor = ''; 
    });

    document.querySelectorAll('.keyboard-key').forEach(key => {
        key.classList.remove('correct', 'present', 'absent');
    });

    const winMessageDiv = document.getElementById('win-message');
    if (winMessageDiv.classList.contains('active')) {
        winMessageDiv.classList.remove('active');
    }

    const solutionsDiv = document.getElementById('possibleSolutions');
    if (solutionsDiv) {
        solutionsDiv.innerHTML = '';
    }

    const wordleRows = document.querySelectorAll('.wordleRow');
    wordleRows.forEach((row, index) => {
        if (index === 0) {
            row.classList.add('active');
        } else {
            row.classList.remove('active');
        }
        row.querySelectorAll('.wordleCell').forEach(cell => cell.removeAttribute('readonly'));
    });

    wordleRows[0].querySelector('.wordleCell').focus();
}

document.addEventListener('DOMContentLoaded', startGame);



function autoTab(currentField) {
    currentField.value = currentField.value.toUpperCase().replace(/[^A-Z]/gi, '');

    if (currentField.value.length >= currentField.maxLength) {
        let next = currentField;
        while ((next = next.nextElementSibling)) {
            if (next.tagName.toLowerCase() === "input") {
                next.focus();
                break;
            }
        }
    }
}


function submitGuess() {
    const activeRow = document.querySelector('.wordleRow.active');
    const guess = Array.from(activeRow.querySelectorAll('.wordleCell'))
                       .map(cell => cell.value.trim().toUpperCase())
                       .join('');

    if (guess.length < 5) {
        alert('Please fill all 5 letters before submitting.');
        return;
    }

    const data = { guess: guess };

    fetch('/check_guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.json();
    })
    .then(data => {
        console.log("Received data:", data); 
    
        if (data.error) {
            showError(data.error);
            shakeRow(activeRow);
            return;
        }
    
        applyFeedback(activeRow, data.feedback);

        if (data.feedback) {
            handleFeedback(data.feedback);
          }
    
        if (Array.isArray(data.possible_solutions)) {
            displayPossibleSolutions(data.possible_solutions);
        } else {
            console.error("possible_solutions is not an array or is empty", data.possible_solutions);
            displayPossibleSolutions(["No Possible Solutions!"]);
        }
    
        if (data.game_over) {
            const isWin = data.feedback.every(f => f === 'green');
            handleGameOver(isWin, data.target_word);
        } else {
            moveToNextRow();
        }
    })
    
    .catch(error => {
        console.error('Error:', error);
        showError(error.toString());
        shakeRow(activeRow);
    });
}

function handleGameOver(isWin, targetWord) {
    const winMessageDiv = document.getElementById('win-message');
    document.getElementById('target-word-display').textContent = isWin ? 
        `Congratulations! The target word was: ${targetWord}.` : 
        `Try again! The target word was: ${targetWord}.`;

    if (isWin) {
        confetti();
    }

    const newGameButton = document.getElementById('new-game-button');
    newGameButton.textContent = "New Game";
    newGameButton.onclick = () => {
        winMessageDiv.classList.remove('active');
        startNewGame(); 
    };

    winMessageDiv.classList.add('active');
}

function displayPossibleSolutions(solutions) {
    console.log('Displaying solutions:', solutions);
    let solutionsDiv = document.getElementById('possibleSolutions');
    if (!solutionsDiv) {
        solutionsDiv = document.createElement('div');
        solutionsDiv.id = 'possibleSolutions';
        solutionsDiv.style.display = 'flex';
        solutionsDiv.style.flexWrap = 'wrap';
        solutionsDiv.style.maxHeight = '200px';
        solutionsDiv.style.overflowY = 'scroll';
        solutionsDiv.style.backgroundColor = '#393939';
        solutionsDiv.style.marginTop = '20px';
        solutionsDiv.style.padding = '10px';
        solutionsDiv.style.width = '80%'; 
        solutionsDiv.style.marginLeft = 'auto'; 
        solutionsDiv.style.marginRight = 'auto'; 
        document.body.appendChild(solutionsDiv);
    }
    solutionsDiv.innerHTML = ''; 

    if (solutions && solutions.length > 0) {
        solutions.forEach(solution => {
            const solutionDiv = document.createElement('div');
            solutionDiv.textContent = solution.toUpperCase(); 
            solutionDiv.style.background = 'white'; 
            solutionDiv.style.color = 'black'; 
            solutionDiv.style.fontWeight = 'bold'; 
            solutionDiv.style.margin = '5px';
            solutionDiv.style.borderRadius = '5px';
            solutionDiv.style.padding = '5px';
            solutionDiv.style.textAlign = 'center'; 
            solutionsDiv.appendChild(solutionDiv);
        });
    } else {
        solutionsDiv.innerHTML = '<div>No Possible Solutions!</div>';
    }
}



function applyFeedback(row, feedback) {
    feedback.forEach((status, index) => {
        const cell = row.querySelectorAll('.wordleCell')[index];
        switch (status) {
            case 'green':
                cell.style.backgroundColor = '#6aaa64';
                break;
            case 'yellow':
                cell.style.backgroundColor = '#c9b458';
                break;
            case 'gray':
            default:
                cell.style.backgroundColor = '#787c7e';
        }
    });
}

function shakeRow(row) {
    row.classList.add('shake');
    setTimeout(() => { row.classList.remove('shake'); }, 820); 
}

function showError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.textContent = message;
    errorDiv.style.color = "red";
    errorDiv.style.position = "fixed";
    errorDiv.style.bottom = "20px";
    errorDiv.style.left = "50%";
    errorDiv.style.transform = "translateX(-50%)";
    document.body.appendChild(errorDiv);

    setTimeout(() => {
        document.body.removeChild(errorDiv);
    }, 2000); 
}

function moveToNextRow() {
    const activeRow = document.querySelector('.wordleRow.active');
    activeRow.classList.remove('active');
    const nextRow = activeRow.nextElementSibling;
    if (nextRow) {
        nextRow.classList.add('active');
        Array.from(nextRow.querySelectorAll('.wordleCell')).forEach(cell => {
            cell.value = '';
            cell.removeAttribute('readonly');
        });
        nextRow.querySelectorAll('.wordleCell')[0].focus();
    }
}

  document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.wordleRow');
    rows.forEach((row, index) => {
        if (index > 0) { // Skip the first row
            Array.from(row.querySelectorAll('.wordleCell')).forEach(cell => {
                cell.setAttribute('readonly', true);
            });
        }
    });
});

function clearActiveRow() {
    const activeRow = document.querySelector('.wordleRow.active');
    if (activeRow) {
        const inputs = activeRow.querySelectorAll('.wordleCell');
        inputs.forEach(input => {
            input.value = ''; 
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.wordleCell').forEach(input => {
        input.addEventListener('keydown', handleBackspace);
    });
});

function handleBackspace(event) {
    if (event.key === 'Backspace' && event.target.value === '') {
        const previous = event.target.previousElementSibling;
        if (previous && previous.classList.contains('wordleCell')) {
            previous.focus();
            previous.value = ''; 
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.wordleCell').forEach(input => {
        input.addEventListener('keydown', handleBackspace);

        input.addEventListener('keydown', function(event) {
            if (event.key === "Enter") {
                submitGuess();
            }
        });
    });
});

function showError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.textContent = message;
    errorDiv.style.color = "black";
    errorDiv.style.position = "fixed";
    errorDiv.style.top = "20px";
    errorDiv.style.left = "50%";
    errorDiv.style.transform = "translateX(-50%)";
    errorDiv.style.backgroundColor = "white";
    errorDiv.style.padding = "10px";
    errorDiv.style.opacity = "1";
    errorDiv.style.transition = "opacity 0.5s ease"; 
    document.body.appendChild(errorDiv);

    setTimeout(() => {
        errorDiv.style.opacity = "0";
    }, 1000);
    document.body.appendChild(errorDiv);

    setTimeout(() => {
        if (document.body.contains(errorDiv)) {
            document.body.removeChild(errorDiv);
        }
    }, 1500); 
}

document.querySelectorAll('.keyboard-key').forEach(key => {
    key.addEventListener('click', () => {
      const letter = key.textContent;
      addLetterToCurrentInput(letter);
    });
  });
  
  function addLetterToCurrentInput(letter) {
    const unfilledInput = document.querySelector('.wordleCell:not([value])');
    if (unfilledInput) {
      unfilledInput.value = letter;
      unfilledInput.dispatchEvent(new Event('input', { bubbles: true }));
      autoTab(unfilledInput);
    }
  }
  
  function updateKeyboard(feedback) {
    feedback.forEach((status, index) => {
      const letter = status.letter.toUpperCase();
      const keyElement = document.querySelector(`.keyboard-key[data-key="${letter}"]`);
      if (keyElement) {
        keyElement.classList.remove('correct', 'present', 'absent');
        keyElement.classList.add(status.class);
      }
    });
  }
  
  function handleFeedback(feedback) {
    feedback.forEach((f, index) => {
      const cell = document.querySelectorAll('.wordleCell')[index];
      const keyElement = document.querySelector(`.keyboard-key[data-key="${cell.value}"]`);
      if (keyElement) {
        keyElement.classList.remove('correct', 'present', 'absent');
        if (f === 'green') {
          keyElement.classList.add('correct');
        } else if (f === 'yellow') {
          keyElement.classList.add('present');
        } else if (f === 'gray') {
          keyElement.classList.add('absent');
        }
      }
    });
  }
  


  

