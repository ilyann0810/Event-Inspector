document.addEventListener('DOMContentLoaded', function () {
    const timeline = document.getElementById('timeline');
    const nextBtn = document.getElementById('nextBtn');
    let currentScrollPosition = 0;
    const itemHeight = document.querySelector('.timeline-item').clientHeight + 20; // item height + margin

    nextBtn.addEventListener('click', function () {
        const maxScrollPosition = timeline.scrollHeight - timeline.clientHeight;
        if (currentScrollPosition < maxScrollPosition) {
            currentScrollPosition += itemHeight;
            if (currentScrollPosition > maxScrollPosition) {
                currentScrollPosition = maxScrollPosition;
            }
            timeline.style.top = -currentScrollPosition + 'px';
        } else {
            // If already at the bottom, reset to the top
            currentScrollPosition = 0;
            timeline.style.top = '0px';
        }
    });
});