// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {form.addEventListener('submit', event => {
      
      function myValidation() {
        const dateStartField = document.getElementById("datecheckin")               
        const dateToday = new Date();
        console.log(dateToday);
        const dateStart = new Date (dateStartField.value);
        if (dateStart < dateToday) {
          dateStartField.classList.add("is-invalid")
          dateStartField.classList.remove("is-valid")
          form.classList.remove('was-validated')
          document.getElementById("datecheckin").value = ""
          return false    
        } else {
          dateStartField.classList.add("is-valid")
          dateStartField.classList.remove("is-invalid")
          return true    
        }

        const dateEndField = document.getElementById("datecheckout")                       
        const dateEnd = new Date (dateStartField.value);
        if (dateEnd < dateStart) {
          dateEndField.classList.add("is-invalid")
          dateEndField.classList.remove("is-valid")
          form.classList.remove('was-validated')
          document.getElementById("datecheckout").value = ""
          return false    
        } else {
          dateEndField.classList.add("is-valid")
          dateEndField.classList.remove("is-invalid")
          return true    
        }




        
      }
    

      

      if (!myValidation() || !form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add('was-validated')
    }, false)
  })
})
()
