document.addEventListener('DOMContentLoaded', function () {
      // Inicialización del Carousel usando Bootstrap
      const myCarouselElement = document.querySelector('#carouselflansindex');
      const carousel = new bootstrap.Carousel(myCarouselElement, {
        interval: 3000,
        touch: false
      });
});
