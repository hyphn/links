$(window).scroll(function () {
	if( $(window).scrollTop() > $('#navbar').offset().top && !($('#navbar').hasClass('fixed'))){
		$('#navbar').addClass('fixed');
	} else if ($(window).scrollTop() <= 200){
		$('#navbar').removeClass('fixed');
	}
});