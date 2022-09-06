var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})


$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})

$('.alert').alert()