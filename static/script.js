function startGame() {
    fetch('/start_game')
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Error starting game:', error));
}

// Call startGame() when the page loads or based on user action
document.addEventListener('DOMContentLoaded', startGame);



function autoTab(currentField) {
    // Convert input to uppercase and remove non-letter characters
    currentField.value = currentField.value.toUpperCase().replace(/[^A-Z]/gi, '');

    // Move to the next field if the current one is filled
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
        console.log("Received data:", data); // Log the entire response
    
        if (data.error) {
            showError(data.error);
            shakeRow(activeRow);
            return;
        }
    
        applyFeedback(activeRow, data.feedback);
    
        // Change this line to match the key sent from Flask
        if (Array.isArray(data.possible_solutions)) {
            displayPossibleSolutions(data.possible_solutions);
        } else {
            console.error("possible_solutions is not an array or is empty", data.possible_solutions);
            displayPossibleSolutions(["No Possible Solutions!"]);
        }
    
        if (data.game_over) {
            alert(data.message || "Game Over!");
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

function displayPossibleSolutions(solutions) {
    console.log('Displaying solutions:', solutions);
    let solutionsDiv = document.getElementById('possibleSolutions');
    if (!solutionsDiv) {
        solutionsDiv = document.createElement('div');
        solutionsDiv.id = 'possibleSolutions';
        solutionsDiv.style.maxHeight = '200px';
        solutionsDiv.style.overflowY = 'scroll';
        solutionsDiv.style.border = '1px solid #ccc';
        solutionsDiv.style.marginTop = '20px';
        solutionsDiv.style.padding = '10px';
        document.body.appendChild(solutionsDiv); // Append wherever it fits in your layout
    }
    solutionsDiv.innerHTML = ''; // Clear previous solutions

    if (solutions && solutions.length > 0) {
        solutions.forEach(solution => {
            const solutionDiv = document.createElement('div');
            solutionDiv.textContent = solution;
            solutionDiv.style.border = '1px solid #ddd';
            solutionDiv.style.margin = '5px';
            solutionDiv.style.padding = '5px';
            solutionsDiv.appendChild(solutionDiv);
        });
    } else {
        solutionsDiv.innerHTML = '<div>No Possible Solutions!</div>'; // Show message when no solutions
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
    setTimeout(() => { row.classList.remove('shake'); }, 820); // Match CSS animation duration
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
    }, 2000); // Message disappears after 2 seconds
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
    // Deactivate all rows except the first one upon loading the page.
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
            input.value = ''; // Clear each input field in the active row
        });
        inputs[0].focus(); // Optional: Refocus on the first cell of the active row
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.wordleCell').forEach(input => {
        input.addEventListener('keydown', handleBackspace);
    });
});

function handleBackspace(event) {
    if (event.key === 'Backspace' && event.target.value === '') {
        // If backspace is pressed and the current input is empty, move to the previous input
        const previous = event.target.previousElementSibling;
        if (previous && previous.classList.contains('wordleCell')) {
            previous.focus();
            previous.value = ''; // Optionally clear the previous input as well
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.wordleCell').forEach(input => {
        input.addEventListener('keydown', handleBackspace);

        // Add an event listener for the Enter key
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


  

