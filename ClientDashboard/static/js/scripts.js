jQuery(document).ready(function() {

    /*
        Background slideshow
    */
    $('.top-content').backstretch("/static/img/backgrounds/1.jpg");

    $('#top-navbar-1').on('shown.bs.collapse', function(){
    	$('.top-content').backstretch("resize");
    });
    $('#top-navbar-1').on('hidden.bs.collapse', function(){
    	$('.top-content').backstretch("resize");
    });

    /*
        Wow
    */
    new WOW().init();

		// otp
		$(".otp_field").hide();
		$(".password_Field").show();
		$('#login_via_otp').on('change', function() {
				if($('#login_via_otp').prop('checked')){
					$(".otp_field").show();
					$(".password_Field").hide();
				}else{
					$(".otp_field").hide();
					$(".password_Field").show();
				}

		});

});


(function() {

  var parent = document.querySelector(".range-slider");
  if(!parent) return;

  var
    rangeS = parent.querySelectorAll("input[type=range]"),
    numberS = parent.querySelectorAll("input[type=number]");

  rangeS.forEach(function(el) {
    el.oninput = function() {
      var slide1 = parseFloat(rangeS[0].value),
        	slide2 = parseFloat(rangeS[1].value);

      if (slide1 > slide2) {
				[slide1, slide2] = [slide2, slide1];
        // var tmp = slide2;
        // slide2 = slide1;
        // slide1 = tmp;
      }

      numberS[0].value = slide1;
      numberS[1].value = slide2;
    }
  });

  numberS.forEach(function(el) {
    el.oninput = function() {
			var number1 = parseFloat(numberS[0].value),
					number2 = parseFloat(numberS[1].value);

      if (number1 > number2) {
        var tmp = number1;
        numberS[0].value = number2;
        numberS[1].value = tmp;
      }

      rangeS[0].value = number1;
      rangeS[1].value = number2;

    }
  });

})();


//client view profile
$('#tab-1').show();
$('#tab-2').hide();
$('#aboutDesigner').addClass('active');

$('#aboutDesigner').click(function(){
  $('#tab-1').show();
  $('#tab-2').hide();
  $('#aboutDesigner').addClass('active');
  $('#projectPhotos').removeClass('active');

});

$('#projectPhotos').click(function(){
  $('#tab-1').hide();
  $('#tab-2').show();
  $('#projectPhotos').addClass('active');
  $('#aboutDesigner').removeClass('active');
});



// gallery popup start
$('#popup-image-gallery').on('shown.bs.modal', function() {
  $('.popup-slider-for').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    fade: true,
    asNavFor: '.popup-slider-nav',

    // adaptiveHeight: true,
  });
  $('.popup-slider-nav').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: '.popup-slider-for',
    dots: false,
    arrows: true,
    focusOnSelect: true,
    variableWidth: true,
    centerMode: true,
    infinite: false,
  });
});
// Slick.js: Get current and total slides (ie. 3/5)
var $status = $('.pagingInfo');
var $slickElement = $('.popup-slider-for');

$slickElement.on('init reInit afterChange', function(event, slick, currentSlide, nextSlide) {
  //currentSlide is undefined on init -- set it to 0 in this case (currentSlide is 0 based)
  var i = (currentSlide ? currentSlide : 0) + 1;
  $status.text(i + '/' + slick.slideCount);
});

// Slick slider sync situation
var slides = $(".popup-slider-for .slick-track > .slick-slide").length;
$('.popup-slider-for').on('afterChange', function(event, slick, currentSlide, nextSlide) {
  var inFocus = $('.popup-slider-for .slick-current').attr('data-slick-index');
  $('.popup-slider-nav .slick-current').removeClass('slick-current');
  $('.popup-slider-nav .slick-slide[data-slick-index="' + inFocus + '"]').trigger('click');
});
// gallery popup ended

// listing page filters start
False = false
True = true
const filtersData = {
                      mordern: False,
                      traditional: False,
                      bohemian: False,
                      budget : {
                        min: 0,
                        max: 0
                      }
                    };


$('#mainFilters').change(function(){
    if ($('#morden_style').prop("checked")) {

        filtersData['mordern'] = True;
    } else {
        filtersData['mordern'] = False;
    }
  if($('#traditional_style').prop("checked")){
      filtersData['traditional'] = True;
  }else{
    filtersData['traditional'] = False;
  }
  if($('#Bohemian_style').prop("checked")){
    filtersData['bohemian'] = True;
  }else{
    filtersData['bohemian'] = False;
  }
  filtersData["budget"].min = $("#rangeMin").val();
  filtersData["budget"].max = $("#rangeMax").val();

  filterValued(filtersData);

});

const filter_div = $('#filtered_result');
const endpoint = window.location.href;
function filterValued(data){
  var filterSaveData = $.ajax({
      type: 'GET',
      url: endpoint,
      data: data,
      dataType: "json",
      success: function(resultData) {
          // console.log(resultData);
          filter_div.html(resultData['html_from_view']);
        console.log("success!");
      }
});
  filterSaveData.error(function() { console.log("failed!")});
}

//listing page filters end