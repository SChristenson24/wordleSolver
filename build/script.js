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
    
    // Example processing the guess
    
    // Deactivate the current row
    activeRow.classList.remove('active');
    Array.from(activeRow.querySelectorAll('.wordleCell')).forEach(cell => {
      cell.setAttribute('readonly', true);
    });
  
    // Activate the next row
    const nextRow = activeRow.nextElementSibling;
    if (nextRow) {
      nextRow.classList.add('active');
      Array.from(nextRow.querySelectorAll('.wordleCell')).forEach(cell => {
        cell.removeAttribute('readonly');
      });
      nextRow.querySelector('.wordleCell').focus(); // Focus on the first cell of the next row
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


  

