// Get the modal
var modal = document.getElementById("imgModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementsByClassName("gallery-thumbnail");
var modalSrc = document.getElementById("modalSrc");
var captionText = document.getElementById("caption");
var onClick = function(e){
  img = e.target.getAttribute('data-val');
  imgCaption = e.target.getAttribute('alt');
  console.log(img);
  console.log(modalSrc);
  modal.style.display = "block";
  modalSrc.src = img;
  captionText.innerHTML = imgCaption;
  //captionText.innerHTML = this.alt;
};

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
var onClose = function() {
  modal.style.display = "none";
}