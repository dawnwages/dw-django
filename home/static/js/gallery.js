/*
 * Page gallery lightbox (home/blocks/gallery.html). Uses a native <dialog>,
 * which gives the backdrop, Esc to close and focus handling for free.
 * Click outside the image to close; arrow keys move between images.
 */
(function () {
  "use strict";

  Array.prototype.forEach.call(document.querySelectorAll("[data-gallery]"), function (root) {
    var items = Array.prototype.slice.call(root.querySelectorAll(".dw-gallery__item"));
    var dialog = root.querySelector(".dw-lightbox");
    if (!items.length || !dialog || !dialog.showModal) return;

    var img = dialog.querySelector(".dw-lightbox__img");
    var caption = dialog.querySelector(".dw-lightbox__caption");
    var current = 0;

    dialog.classList.toggle("is-single", items.length < 2);

    function show(index) {
      current = (index + items.length) % items.length;
      var item = items[current];
      img.src = item.getAttribute("data-src");
      img.alt = item.getAttribute("data-caption") || "";
      caption.textContent = item.getAttribute("data-caption") || "";
      caption.hidden = !caption.textContent;
    }

    items.forEach(function (item, i) {
      item.addEventListener("click", function () {
        show(i);
        dialog.showModal();
        document.documentElement.classList.add("dw-lightbox-open");
      });
    });

    dialog.addEventListener("close", function () {
      document.documentElement.classList.remove("dw-lightbox-open");
      items[current].focus();
    });

    dialog.addEventListener("click", function (event) {
      var step = event.target.closest("[data-step]");
      if (step) return show(current + Number(step.getAttribute("data-step")));
      // Close on the close button or a click anywhere that isn't the image.
      if (event.target.closest("[data-close]") || !event.target.closest(".dw-lightbox__img")) {
        dialog.close();
      }
    });

    dialog.addEventListener("keydown", function (event) {
      if (items.length < 2) return;
      if (event.key === "ArrowRight") show(current + 1);
      if (event.key === "ArrowLeft") show(current - 1);
    });
  });
})();
