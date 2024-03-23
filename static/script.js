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
    // Collect the guess
    const activeRow = document.querySelector('.wordleRow.active');
    const guess = Array.from(activeRow.querySelectorAll('.wordleCell'))
                       .map(cell => cell.value.trim().toUpperCase())
                       .join('');

    if (guess.length < 5) {
        alert('Please fill all 5 letters before submitting.');
        return;
    }

    // Example data structure, adjust according to your actual logic
    const data = {
        guess: guess, // Adjusted to send the guess directly
        // Add more data if needed
    };

    // Send the guess to the server
    fetch('/check_guess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(feedback => {
        // Apply color feedback to each cell
        feedback.forEach((status, index) => {
            const cell = activeRow.querySelectorAll('.wordleCell')[index];
            let color;
            switch (status) {
                case 'green':
                    color = '#6aaa64'; // Example color for correct letters
                    break;
                case 'yellow':
                    color = '#c9b458'; // Example color for present but wrong position letters
                    break;
                case 'gray':
                default:
                    color = '#787c7e'; // Example color for absent letters
            }
            cell.style.backgroundColor = color;
            cell.style.color = 'white'; // Example, adjust as needed
        });

        // Prepare for the next guess
        moveToNextRow();
    })
    .catch(error => console.error('Error:', error));
}

function moveToNextRow() {
    const activeRow = document.querySelector('.wordleRow.active');
    activeRow.classList.remove('active');
    activeRow.setAttribute('readonly', true); // Prevent further typing in the current row

    const nextRow = activeRow.nextElementSibling;
    if (nextRow) {
      nextRow.classList.add('active');
      Array.from(nextRow.querySelectorAll('.wordleCell')).forEach(cell => {
        cell.removeAttribute('readonly');
        cell.value = ''; // Clear the cell for the new guess
      });
      nextRow.querySelectorAll('.wordleCell')[0].focus(); // Focus the first cell of the next row
    } else {
        // Handle end of game, such as displaying a message or disabling input
        alert("End of game!");
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


  

