//  these scripts are used for various function inside materilize css
$(document).ready(function () {
  $(".carousel").carousel({
    fullWidth: true,
    indicators: true,
    duration: 200,
  });
  // function for next slide
  $(".next").click(function () {
    $(".carousel").carousel("next");
  });

  // function for prev slide
  $(".prev").click(function () {
    $(".carousel").carousel("prev");
  });

  // modal
  $(".modal").modal();

  // Initialize materialize data picker
  $(".datepicker").datepicker({ format: "yyyy-mm-dd" });
  $("select").formSelect();

  $(".timepicker").timepicker({
    twelveHour: false,
  });

  $(".sidenav").sidenav();

  $(".mobile-submenu").sidenav({
    edge: "right",
  });

  $(".dropdown-trigger").dropdown({
    coverTrigger: false,
    // hover: true,
  });
});

function scrollSmoothTo(elementId) {
  yOffset = -10;
  element = document.getElementById(elementId);
  y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
  var element = document.getElementById(elementId);
  element.scrollIntoView({
    block: "center",
    behavior: "smooth",
  });
}
