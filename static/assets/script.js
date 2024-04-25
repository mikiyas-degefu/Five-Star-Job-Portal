$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  var modal = $(this)
  modal.find('.modal-title').text('New message to ' + recipient)
  modal.find('.modal-body input').val(recipient)
})


function activeModalApplyJob(getId){
  modal = `
  <div class="modal fade" id="apply__job${getId}" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="apply__job${getId}Label" aria-hidden="true">
   <div class="modal-dialog">
     <div class="modal-content">
       <div class="modal-header">
         <h5 class="modal-title" id="apply__job${getId}Label">Are you sure you want to delete</h5>
         <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
       </div>
       <div class="modal-body h3">
         {{form.title.value}}?
       </div>
       <div class="modal-footer">
         <button type="button" class="btn btn-muted" data-bs-dismiss="modal">Close</button>
         <form action="" method="post">
           {% csrf_token %}
         <a href="{% url 'delete-department-admin' job.id %}" type="submit" class="btn btn-danger">Yes</a>
       </form>
       </div>
     </div>
   </div>
  </div>`
  document.getElementById("modal_apply_job").innerHTML = modal
  location.reload();
  document.addEventListener("DOMContentLoaded", function() {
    var button = document.getElementById(getId);
    button.click();
  });
}
