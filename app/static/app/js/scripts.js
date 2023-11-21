
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

// Notificação
document.addEventListener("DOMContentLoaded", function() {
  // Verifica se há um novo post desde a última notificação
  if (isNewPost()) {
    showNotification();

    // Ocultar a notificação após alguns segundos
    setTimeout(function() {
      hideNotification();
    }, 3000); // 3000 milissegundos (3 segundos)
  }
});

function isNewPost() {
  // Obtém o número total de posts
  var totalPosts = document.querySelectorAll('.criadoem').length;

  // Obtém a quantidade de posts registrados na última notificação
  var lastNotificationCount = localStorage.getItem('lastNotificationCount') || 0;

  // Verifica se a notificação deve ser exibida
  var newPosts = totalPosts > lastNotificationCount;

  // Atualiza a quantidade registrada na última notificação apenas se houver novos posts
  if (newPosts) {
    localStorage.setItem('lastNotificationCount', totalPosts);
  }

  return newPosts;
}

function showNotification() {
  var notification = document.getElementById("index-notification");
  notification.style.display = "block";

  // Força o reflow antes de adicionar a classe para ativar a transição
  void notification.offsetWidth;

  // Adiciona a classe para exibir a notificação suavemente
  notification.style.opacity = 1;
}

function hideNotification() {
  var notification = document.getElementById("index-notification");

  // Remove a classe para ocultar a notificação suavemente
  notification.style.opacity = 0;

  // Oculta completamente a notificação após a transição
  setTimeout(function() {
    notification.style.display = "none";
  }, 500); // Tempo correspondente à duração da transição (500 milissegundos)
}

// Confirmação para apagar os Posts:
function confirmDelete(title, postId) {
  Swal.fire({
    title: 'Confirmação',
    text: `Você tem certeza de que deseja excluir o post '${title}'?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#4E4FEB',
    confirmButtonText: 'Sim, Excluir!',
    cancelButtonText: 'Cancelar',
    customClass: {
      container: 'custom-swal-container', // Classe para o contêiner principal
      popup: 'custom-swal-popup', // Classe para o contêiner da caixa de diálogo
      header: 'custom-swal-header', // Classe para o cabeçalho
      title: 'custom-swal-title', // Classe para o título
      closeButton: 'custom-swal-close-button', // Classe para o botão de fechar
      icon: 'custom-swal-icon', // Classe para o ícone
      content: 'custom-swal-content', // Classe para o conteúdo
      input: 'custom-swal-input', // Classe para a entrada (se aplicável)
      actions: 'custom-swal-actions', // Classe para os botões de ação
      confirmButton: 'custom-swal-confirm-button', // Classe para o botão de confirmação
      cancelButton: 'custom-swal-cancel-button', // Classe para o botão de cancelamento
      footer: 'custom-swal-footer' // Classe para o rodapé
    }
  }).then((result) => {
    if (result.isConfirmed) {
      // Se o usuário confirmar, envie o formulário de exclusão
      document.getElementById('deleteForm' + postId).submit();
    }
  });
}

document.addEventListener('DOMContentLoaded', function() {
  var fileInput = document.querySelector('[type="file"]');
  if (fileInput) {
      fileInput.addEventListener('change', function() {
          var resetButton = this.form.querySelector('[type="reset"]');
          if (resetButton) {
              resetButton.remove();
          }
      });
  }
});
/////SSublinhado register
document.getElementById('register-link').addEventListener('mouseover', function() {
  this.style.textDecoration = 'underline';
});

// Adiciona um ouvinte de evento para remover o sublinhado ao retirar o mouse
document.getElementById('register-link').addEventListener('mouseout', function() {
  this.style.textDecoration = 'none';
});

document.addEventListener('DOMContentLoaded', function () {
  const likeHeart = document.querySelector('.like-heart');

  likeHeart.addEventListener('click', function () {
      console.log('Clique no coração');
      likeHeart.classList.toggle('active');
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const likeButtons = document.querySelectorAll('.like-heart');

  likeButtons.forEach(button => {
      button.addEventListener('click', async function () {
          const postId = this.getAttribute('data-post-id');
          const likeCountElement = document.getElementById(`like-count-${postId}`);
          
          try {
              const response = await fetch(`/like/${postId}/`, {
                  method: 'POST',
              });

              if (!response.ok) {
                  throw new Error('Não foi possível curtir o post.');
              }

              // Simule a alteração visual do ícone de coração
              this.classList.toggle('filled');

              // Simule o aumento do contador de curtidas
              const currentLikeCount = parseInt(likeCountElement.innerText, 10);
              const newLikeCount = currentLikeCount + 1;
              likeCountElement.innerText = newLikeCount;
          } catch (error) {
              console.error(error.message);
          }
      });
  });
});