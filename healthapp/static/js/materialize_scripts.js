//  these scripts are used for various function inside materilize css

console.log("test");
$(document).ready(function () {
  $(".carousel").carousel({
    fullWidth: true,
    indicators: true,
    duration: 100,
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
  $(".collapsible").collapsible();

  $(".button-collapse").sidenav();

  $(".collapsible").collapsible();

  $("select").formSelect();

  $(".parallax").parallax();

  $(".tooltipped").tooltip();
});

// interval for homepage carousel
setInterval(function () {
  $(".carousel").carousel("next");
}, 12000); // every 12 seconds
