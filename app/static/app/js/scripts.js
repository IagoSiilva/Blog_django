
// const floatingButton = document.getElementById('floatingButton');

// floatingButton.addEventListener('mouseover', () => {
//     floatingButton.style.width = '200px';
//     floatingButton.style.backgroundColor = '#0056b3';
// });

// floatingButton.addEventListener('mouseout', () => {
//     floatingButton.style.width = '50px';
//     floatingButton.style.backgroundColor = '#007BFF';
// });

document.querySelector('form').addEventListener('submit', function(event) {
    var commentText = document.querySelector('#comment-text').value;

    if (commentText.trim() === '') {
        event.preventDefault(); // Impede o envio do formulário
        document.querySelector('#comment-error').classList.remove('d-none'); // Exibe a mensagem de erro
    }
});