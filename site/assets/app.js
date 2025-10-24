// Custom JavaScript for the site
document.addEventListener('DOMContentLoaded', function() {
    console.log('Slartibartfast site loaded successfully!');

    // Add smooth scroll behavior to anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
