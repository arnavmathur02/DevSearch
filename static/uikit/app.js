// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});


let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

if (alertWrapper) {
  console.log('Alert Wrapper Clicked')
  alertClose.asddEventListner('click', () => 
  alertWrapper.style.display = 'none'
  )
}
