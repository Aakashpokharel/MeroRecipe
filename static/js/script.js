// init Isotope
var $grid = $('.collection-list').isotope({
  // options
});
// filter items on button click
$('.filter-button-group').on('click', 'button', function () {
  var filterValue = $(this).attr('data-filter');
  resetFilterBtns();
  $(this).addClass('active-filter-btn');
  $grid.isotope({ filter: filterValue });
});

var filterBtns = $('.filter-button-group').find('button');
function resetFilterBtns() {
  filterBtns.each(function () {
    $(this).removeClass('active-filter-btn');
  });
}

//Ratings
// script.js

document.addEventListener("DOMContentLoaded", function () {
  const stars = document.querySelectorAll(".star");
  const ratingInput = document.querySelector("#id_value");

  stars.forEach((star, index) => {
    star.addEventListener("click", () => {
      ratingInput.value = index + 1;
      highlightStars(index);
    });

    star.addEventListener("mouseover", () => {
      highlightStars(index);
    });

    star.addEventListener("mouseout", () => {
      highlightStars(ratingInput.value - 1);
    });
  });

  function highlightStars(index) {
    stars.forEach((star, i) => {
      if (i <= index) {
        star.classList.add("active");
      } else {
        star.classList.remove("active");
      }
    });
  }
});

$(document).ready(function () {
  $('.star').click(function () {
    $(this).addClass('checked');
    $(this).prevAll('.star').addClass('checked');
    $(this).nextAll('.star').removeClass('checked');
  });
});
