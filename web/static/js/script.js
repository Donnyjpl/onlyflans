
  document.addEventListener('DOMContentLoaded', function() {
      const myCarouselElement = document.querySelector('#carouselflansindex');
      const carousel = new bootstrap.Carousel(myCarouselElement, {
          interval: 3000,
          touch: false
      });
  });
