function autoTab(currentField) {
    // Move to the next field if the current one is filled
    if (currentField.value.length >= currentField.maxLength) {
        let next = currentField;
        while (next = next.nextElementSibling) {
            if (next.tagName.toLowerCase() === "input") {
                next.focus();
                break;
            }
        }
    }
}

function submitGuess() {
    // Collect the current guess
    const currentRow = document.querySelector('.wordleRow:last-child');
    const guess = Array.from(currentRow.querySelectorAll('.wordleCell'))
                       .map(cell => cell.value.trim().toUpperCase())
                       .join('');
    
    // Validate guess length
    if (guess.length < 5) {
        alert('Please fill all 5 letters before submitting.');
        return;
    }

}
