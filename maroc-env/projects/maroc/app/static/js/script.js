let navbar=document.querySelector('.header .navbar');
let menuBtn=document.querySelector('#menu-btn');

menuBtn.onclick = () => {
    menuBtn.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

var swiper = new Swiper(".home-slider", {
    grabCursor:true,
    loop:true,
    centeredSLides:true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
});

var swiper = new Swiper(".food-slider", {
    grabCursor:true,
    loop:true,
    centeredSLides:true,
    spaceBetween: 20,
    pagination: {
        el: ".swiper-pagination",
        clickable: true
      },
    breakpoints: {
        0: {
          slidesPerView: 1,
        },
        700: {
          slidesPerView: 2,
        },
        1000: {
          slidesPerView: 3,
        },
    },
});

