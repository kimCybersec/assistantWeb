function toggleDay(day) {
    const element = document.getElementById(`${day}-content`);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
  const dayButtons = document.querySelectorAll('.day-btn');
  
  dayButtons.forEach(button => {
    button.addEventListener('click', function() {
      document.querySelectorAll('.day-content').forEach(content => {
        if (content !== this.nextElementSibling) {
          content.classList.remove('active');
          this.previousElementSibling?.classList?.remove('active');
        }
      });
      
      const content = this.nextElementSibling;
      content.classList.toggle('active');
      this.classList.toggle('active');
    });
  });
});