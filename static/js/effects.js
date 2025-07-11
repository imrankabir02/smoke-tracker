document.addEventListener('DOMContentLoaded', () => {
    const logSmokeButton = document.getElementById('log-smoke-btn');
    const fireContainer = document.getElementById('fire-container');

    if (logSmokeButton && fireContainer) {
        logSmokeButton.addEventListener('click', (event) => {
            // Prevent the link from navigating immediately
            event.preventDefault();

            // Create particles
            createParticles(fireContainer, 30, 30);

            // Allow the navigation to proceed after the animation has had time to start
            setTimeout(() => {
                window.location.href = logSmokeButton.href;
            }, 4000);
        });
    }

    function createParticles(container, num, leftSpacing) {
        // Clear any existing particles
        container.innerHTML = '';

        for (let i = 0; i < num; i += 1) {
            let particle = document.createElement('div');
            particle.style.left = `calc((100% - 5em) * ${i / leftSpacing})`;
            particle.setAttribute('class', 'particle');
            particle.style.animationDelay = Math.random() * 0.5 + 's';
            container.appendChild(particle);
        }
    }
});
