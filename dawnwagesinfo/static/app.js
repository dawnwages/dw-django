document.addEventListener('DOMContentLoaded', () => {
  // Get all dropdowns on the page
  const dropdowns = document.querySelectorAll('.dropdown');

  dropdowns.forEach(dropdown => {
    const dropdownButton = dropdown.querySelector('.dropdown-toggle');
    const dropdownMenu = dropdown.querySelector('.dropdown-menu');

    // Toggle the dropdown menu on button click
    dropdownButton.addEventListener('click', (event) => {
      // Prevent the click from propagating to the window and immediately closing
      event.stopPropagation();
      dropdown.classList.toggle('show');
    });
  });

  // Close dropdowns if the user clicks outside
  window.addEventListener('click', (event) => {
    dropdowns.forEach(dropdown => {
      if (!dropdown.contains(event.target)) {
        dropdown.classList.remove('show');
      }
    });
  });
});