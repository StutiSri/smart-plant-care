const openModalButtons = document.querySelectorAll('[data-modal-target]')
const overlay = document.getElementById('overlay');

openModalButtons.forEach(button => {
  button.addEventListener('click', function (e) {
    const modal = document.querySelector(button.dataset.modalTarget)
    openModal(modal);
  })
});

overlay.addEventListener('click', () => {
  const modals = document.querySelectorAll('.modalcls.active')
  modals.forEach(modal => {
    closeModal(modal)
  })
})

const confirmButton = document.getElementById('form');
confirmButton.addEventListener('submit', function (e) {
  e.preventDefault();
  var url = $(this).closest('form').attr('action');
  const incorrectCredsError = document.getElementById('creds-error');
  incorrectCredsError.classList.remove('active')

  const username = document.getElementById('username').value
  const password = document.getElementById('password').value

  fetch(url, {
    method: 'POST',
    body: JSON.stringify({
      "username": username,
      "password": password
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
    .then(function (response) {
      if (response.ok) {
        const modal = confirmButton.closest('.modalcls')
        closeModal(modal)
        const successMessage = document.querySelector('.success-message')
        successMessage.classList.add('active');
        return;
      } else if (response.status == "401") {
        incorrectCredsError.classList.add('active')
      }
      throw new Error('Failed to initiate command.');
    })
    .catch(function (error) {
      console.log(error);
    });

});

function openModal(modal) {
  if (modal == null) return;
  modal.classList.add('active');
  overlay.classList.add('active');
}

function closeModal(modal) {
  if (modal == null) return;
  modal.classList.remove('active');
  overlay.classList.remove('active');
}