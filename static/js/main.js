jQuery(document).ready(function() {
  $("#btn-triangle-left").click(function(e) {
    e.preventDefault();
    console.log("helloWorld!");
    $(".btnText").fadeToggle(50);
    $("#sidebar-wrapper").toggleClass("sidebar-wrapper-toggled");
    $("#sidebar-nav li a").toggleClass("sidebar-nav-toggle");
    $("#sidebar-nav li a .imgs").toggleClass("sideImageToggle");
    $("#btn-triangle-left").toggleClass("btn-triangle-right");
  });
});
