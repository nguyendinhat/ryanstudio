/*
 * M-Store | Modern E-Commerce Template
 * Copyright 2016 rokaux
 * Theme Custom Scripts
 */
function formatMoney(n) {	
	return n.toFixed(0).replace(/./g, function(c, i, a) {
        return i > 0 && c !== "." && (a.length - i) % 3 === 0 ? "." + c : c;
    })+" ₫";
}

var footerHeight = 0, footerTop = 0, $footer = $("#footer");
function positionFooter() {	
	footerHeight = $footer.height();
	footerTop = ($(window).scrollTop()+$(window).height()-footerHeight)+"px";	
	if ( ($(document.body).height()+footerHeight) < $(window).height()) {
		$footer.css({
				position: "absolute"
		}).animate({
				top: footerTop
		}, 0);
	} else {
		$footer.css({
				position: "static"
		});
	}
}
positionFooter();
$(window).scroll(positionFooter).resize(positionFooter);


jQuery(document).ready(function($) {
	'use strict';	// Check if Page Scrollbar is visible
	//------------------------------------------------------------------------------
	var hasScrollbar = function() {
	// The Modern solution
	if (typeof window.innerWidth === 'number') {
		return window.innerWidth > document.documentElement.clientWidth;
	}

		// rootElem for quirksmode
	var rootElem = document.documentElement || document.body;

	// Check overflow style property on body for fauxscrollbars
	var overflowStyle;

	if (typeof rootElem.currentStyle !== 'undefined') {
			overflowStyle = rootElem.currentStyle.overflow;
	}

	overflowStyle = overflowStyle || window.getComputedStyle(rootElem, '').overflow;

		// Also need to check the Y axis overflow
	var overflowYStyle;

	if (typeof rootElem.currentStyle !== 'undefined') {
			overflowYStyle = rootElem.currentStyle.overflowY;
	}

	overflowYStyle = overflowYStyle || window.getComputedStyle(rootElem, '').overflowY;

	var contentOverflows = rootElem.scrollHeight > rootElem.clientHeight;
	var overflowShown    = /^(visible|auto)$/.test(overflowStyle) || /^(visible|auto)$/.test(overflowYStyle);
	var alwaysShowScroll = overflowStyle === 'scroll' || overflowYStyle === 'scroll';

		return (contentOverflows && overflowShown) || (alwaysShowScroll);
	};
	if (hasScrollbar()) {
		$('body').addClass('hasScrollbar');
	}


	// Disable default link behavior for dummy links that have href='#'
	//------------------------------------------------------------------------------
	var $emptyLink = $('a[href=#]');
	$emptyLink.on('click', function(e){
		e.preventDefault();
	});


	// Page Transitions
	if($('.page-preloading').length) {
		$('a:not([href^="#"])').on('click', function(e) {
	    if($(this).attr('class') !== 'video-popup-btn' && $(this).attr('class') !== 'gallery-item' && $(this).attr('class') !== 'ajax-post-link' && $(this).attr('class') !== 'read-more ajax-post-link') {
				console.log($(this).attr('class'));
			e.preventDefault();
			var linkUrl = $(this).attr('href');
			$('.page-preloading').addClass('link-clicked');
			setTimeout(function(){
				window.open(linkUrl , '_self');
			}, 550);
			}
		});
	}


	// Animated Scroll to Top Button
	//------------------------------------------------------------------------------
	var $scrollTop = $('.scroll-to-top-btn');
	if ($scrollTop.length > 0) {
		$(window).on('scroll', function(){
	    if ($(window).scrollTop() > 600) {
			$scrollTop.addClass('visible');
		} else {
			$scrollTop.removeClass('visible');
		}
		});
		$scrollTop.on('click', function(e){
			e.preventDefault();
			$('html').velocity("scroll", { offset: 0, duration: 1000, easing:'easeOutExpo', mobileHA: false });
		});
	}


	// Smooth scroll to element
	//------------------------------------------------------------------------------
	var $scrollTo = $('.scroll-to');
	$scrollTo.on('click', function(event) {
		var $elemOffsetTop = $(this).data('offset-top');
		$('html').velocity("scroll", { offset:$(this.hash).offset().top-$elemOffsetTop, duration: 1000, easing:'easeOutExpo', mobileHA: false});
		event.preventDefault();
	});


	// Language Dropdown
	//------------------------------------------------------------------------------
	var langSwitcher = $('.lang-switcher'),
			langToggle = $('.lang-toggle');
	langToggle.on('click', function() {
		$(this).parent().toggleClass('open');
	});
	langSwitcher.on('click', function(e) {
    e.stopPropagation();
	});
	$(document).on('click', function(e) {
		langSwitcher.removeClass('open');
	});


	// Toggle Mobile Menu
	//------------------------------------------------------------------------------
	var menuToggle = $('.mobile-menu-toggle'),
			mobileMenu = $('.main-navigation');
	menuToggle.on('click', function() {
		$(this).toggleClass('active');
		mobileMenu.toggleClass('open');
	});


	// Toggle Submenu
	//------------------------------------------------------------------------------
	var $hasSubmenu = $('.menu-item-has-children > a');

	function closeSubmenu() {
		$hasSubmenu.parent().removeClass('active');
	}
	$hasSubmenu.on('click', function(e) {
		if($(e.target).parent().is('.active')) {
			closeSubmenu();
		} else {
			closeSubmenu();
			$(this).parent().addClass('active');
		}
	});

	//  toogle nar
	// ----------------------------------------------------------------------------
	$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
		var target = $(e.target).attr("href"); // activated tab
		if (target=='#newcomers'||target=='#profile') {
			$("#tab-1").addClass("active");
			$("#tab-2").removeClass("active");
			$("#tab-3").removeClass("active");
		}
		if (target=='#toprated'||target=='#status-order') {
			$("#tab-1").removeClass("active");
			$("#tab-2").addClass("active");
			$("#tab-3").removeClass("active");
		}
		if (target=='#onsale') {        
			$("#tab-1").removeClass("active");
			$("#tab-2").removeClass("active");
			$("#tab-3").addClass("active");
		}
	});
	// Isotope Grid / Filters (Gallery)
	//------------------------------------------------------------------------------
	$(window).on('load', function(){

		// Isotope Grid
		var $grid = $('.isotope-grid');
		if($grid.length > 0) {
			$grid.isotope({
				itemSelector: '.grid-item',
			});
			setTimeout( function () {
				$grid.isotope( 'layout' );
			}, 1 );
		}

		// Filtering
		if($('.filter-grid').length > 0) {
			var $filterGrid = $('.filter-grid');
			$('.nav-filters').on( 'click', 'a', function(e) {
				e.preventDefault();
				$('.nav-filters li').removeClass('active');
				$(this).parent().addClass('active');
				var $filterValue = $(this).attr('data-filter');
				$filterGrid.isotope({ filter: $filterValue });
			});
		}
	});


	// Shop Filters Toggle
	//------------------------------------------------------------------------------
	var filtersToggle = $('[data-toggle="filters"]'),
			filtersWrap = $('.filters'),
			filtersPane = $('.filters-pane');
	function closeFilterPane() {
		filtersToggle.removeClass('active');
		filtersPane.removeClass('open');
		filtersWrap.css('height', 0);
	}
	filtersToggle.on('click', function(e) {
		var currentFilter = $(this).attr('href');
		if($(this).is('.active')) {
			closeFilterPane();
		} else {
			closeFilterPane();
			$(this).addClass('active');
			filtersWrap.css('height', $(currentFilter).outerHeight());
			$(currentFilter).addClass('open');
		}
		e.preventDefault();
	});
	if(typeof window.Modernizr !== "undefined" && !Modernizr.touch) {
		$(window).on('resize', function() {
			closeFilterPane();
		});
	}

	// Sidebar Toggle on Mobile
	//------------------------------------------------------------------------------
	var sidebar = $('.sidebar'),
			sidebarToggle = $('.sidebar-toggle');
	sidebarToggle.on('click', function() {
		$(this).addClass('sidebar-open');
		sidebar.addClass('open');
	});
	$('.sidebar-close').on('click', function() {
		sidebarToggle.removeClass('sidebar-open');
		sidebar.removeClass('open');
	});


	// Waves Effect (on Buttons)
	
	//------------------------------------------------------------------------------
	if($('.waves-effect').length) {
		Waves.displayEffect( { duration: 600 } );
	}
	// Product Gallery
	//------------------------------------------------------------------------------
	var galleryThumb = $('.product-gallery-thumblist a'),
			galleryPreview = $('.product-gallery-preview > li');

	// Thumbnails
	//------------------------------------------------------------------------------
	galleryThumb.on('click', function(e) {
		var target = $(this).attr('href');

		galleryThumb.parent().removeClass('active');
		$(this).parent().addClass('active');
		galleryPreview.removeClass('current');
		$(target).addClass('current');

		e.preventDefault();
	});


	// Color Select
	//------------------------------------------------------------------------------
	$('.color-select').on('change', function() {
		var target = $(this).find(':selected').data('image');
		$('[href="#' + target + '"]').trigger('click');
	});


	// Single Post via Ajax
	//------------------------------------------------------------------------------
	var ajaxPostLink = $('.ajax-post-link'),
			postBackdrop = $('.single-post-backdrop'),
			postContainer = $('.single-post-wrap'),
			postContentWrap = $('.single-post-wrap .inner'),
			postContent = $('.single-post-wrap .inner .post-content'),
			closeBtn = $('.single-post-wrap .close-btn'),
			postPreloader = $('.single-post-wrap .preloader');

	// Get Data via Ajax
	function getData(url) {
		$.ajax({
			url: url,
			type: "GET",
			dataType: "html",
			success: successFn,
			error: errorFn,
			complete: function(xhr, status) {
				console.log('Request is complete!');
			}
		});
	}

	// Success
	function successFn(result, status) {
		postContent.prepend(result);
		postContentWrap.addClass('loaded');
		console.log('Data has been received!');
	}

	// Error
	function errorFn(xhr, status, strErr) {
		postContent.prepend('<p>' + strErr + '</p>');
		postContentWrap.addClass('loaded');
		console.log(strErr);
	}

	// Open Post
	function openPost(postUrl) {

		$('body').addClass('blog-post-open');
		postBackdrop.addClass('active');
		postContainer.addClass('open');
		postPreloader.addClass('active');

		setTimeout(function() {
			postPreloader.removeClass('active');
			getData(postUrl);
		}, 900);
	}

	// Close Post
	function closePost() {
		$('body').removeClass('blog-post-open');
		postBackdrop.removeClass('active');
		postContainer.removeClass('open');
		postContentWrap.removeClass('loaded');
		setTimeout(function() {
			postContent.empty();
		}, 500);
	}

	ajaxPostLink.on('click', function(e) {
		var targetPost = $(this).attr('href');

		openPost(targetPost);

		e.preventDefault();
	});

	closeBtn.on('click', closePost);

	// Input-100
	function showValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).addClass('alert-validate');
    }
    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }     
    $('.input100').each(function(){
        $(this).focus(function(){
            hideValidate(this);
        });
    });    
    $('.selection-2').each(function(){
        $(this).change(function(){
            hideValidate(this);
        });
    }); 
	$('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        });    
    });
	$('.selection-2').each(function(){
        $(this).change(function(){
			if ($(this).find(':selected').attr("rel")==-1){
                $(this).removeClass('has-val');
            } else {                
                $(this).addClass('has-val');
            }
        });    
	});
	// icheck
	// -----------------------------------------------------------------------------
	$(document).ready(function(){
		$('input[type="checkbox"], input[type="radio"]').iCheck({
			checkboxClass: 'icheckbox_flat-green',
			radioClass: 'iradio_flat-green'
		}); 
	});
	// Tooltips
	//------------------------------------------------------------------------------
	var $tooltip = $('[data-toggle="tooltip"]');
	if ( $tooltip.length > 0 ) {
		$tooltip.tooltip();
	}

	// Countdown Function
	//------------------------------------------------------------------------------
	function countDownFunc( items, trigger ) {
		items.each( function() {
			var countDown = $(this),
					dateTime = $(this).data('date-time');

			var countDownTrigger = ( trigger ) ? trigger : countDown;
			countDownTrigger.downCount({
			date: dateTime,
			offset: +10
			});
		});
	}
	countDownFunc( $('.countdown') );


	// Image Carousel
	//------------------------------------------------------------------------------
	var $imageCarousel = $( '.image-carousel .inner' );
	if ( $imageCarousel.length > 0 ) {
		$imageCarousel.each( function () {

			var dataLoop 	 = $( this ).parent().data( 'loop' ),
					autoPlay   = $( this ).parent().data( 'autoplay' ),
					timeOut    = $( this ).parent().data( 'interval' ),
					autoheight = $( this ).parent().data( 'autoheight' ),
					dataDots 	 = $( this ).parent().data( 'dots' );

			$( this ).owlCarousel( {
				items: 1,
				loop: dataLoop,
				margin: 0,
				nav: true,
				dots: dataDots,
				navText: [ , ],
				autoplay: autoPlay,
				autoplayTimeout: timeOut,
				autoHeight: autoheight
			} );
		} );
	}


	// Hero Slider
	//------------------------------------------------------------------------------
	var $heroSlider = $( '.hero-slider .inner' );
	if ( $heroSlider.length > 0 ) {
		$heroSlider.each( function () {

		var	loop = $(this).parent().data('loop'),
				autoplay = $(this).parent().data('autoplay'),
				interval = $(this).parent().data('interval') || 3000;

			$(this).owlCarousel({
				items: 1,
				loop: loop,
				margin: 0,
				nav: true,
				dots: true,
				navText: [ , ],
				autoplay: autoplay,
				autoplayTimeout: interval,
				autoplayHoverPause: true,
				smartSpeed: 450
			});
		});
	}


	// Video Popup
	//------------------------------------------------------------------------------
	var $videoBtn = $( '.video-popup-btn, .gallery-video, .video-popup-placeholder .play-btn' );
	if( $videoBtn.length > 0 ) {
		$videoBtn.magnificPopup( {
			type: 'iframe',
			mainClass: 'mfp-fade',
			removalDelay: 500,
			gallery: {
				enabled: true
			}
		} );
	}


	// Gallery Popup
	//------------------------------------------------------------------------------
	var $galleryItem = $( '.gallery-item' );
	if( $galleryItem.length > 0 ) {
		$galleryItem.magnificPopup( {
			type: 'image',
			mainClass: 'mfp-fade',
			removalDelay: 500,
			gallery: {
				enabled: true
			}
		} );
	}


	// Range Slider
	//------------------------------------------------------------------------------
	var rangeSlider  = document.querySelector('.ui-range-slider');
	if(typeof rangeSlider !== 'undefined' && rangeSlider !== null) {
		var dataStartMin = parseInt(rangeSlider.parentNode.getAttribute( 'data-start-min' ), 10),
				dataStartMax = parseInt(rangeSlider.parentNode.getAttribute( 'data-start-max' ), 10),
				dataMin 		 = parseInt(rangeSlider.parentNode.getAttribute( 'data-min' ), 10),
				dataMax   	 = parseInt(rangeSlider.parentNode.getAttribute( 'data-max' ), 10),
				dataStep  	 = parseInt(rangeSlider.parentNode.getAttribute( 'data-step' ), 10);
		var valueMin 			= document.querySelector('.ui-range-value-min span'),
				valueMax 			= document.querySelector('.ui-range-value-max span'),
				valueMinInput = document.querySelector('.ui-range-value-min input'),
				valueMaxInput = document.querySelector('.ui-range-value-max input');
		noUiSlider.create(rangeSlider, {
			start: [ dataStartMin, dataStartMax ],
			connect: true,
			step: dataStep,
			range: {
				'min': dataMin,
				'max': dataMax
			}
		});
		rangeSlider.noUiSlider.on('update', function(values, handle) {
			var value = values[handle];
			if ( handle ) {
				valueMax.innerHTML  = formatMoney(Math.round(value));
				valueMaxInput.value = formatMoney(Math.round(value));
			} else {
				valueMin.innerHTML  = formatMoney(Math.round(value));
				valueMinInput.value = formatMoney(Math.round(value));
			}
		});

	}


	// Google Maps API
	//------------------------------------------------------------------------------
	var $googleMap = $('.google-map');
	if($googleMap.length > 0) {
		$googleMap.each(function(){
			var mapHeight = $(this).data('height'),
					address = $(this).data('address'),
					zoom = $(this).data('zoom'),
					controls = $(this).data('disable-controls'),
					scrollwheel = $(this).data('scrollwheel'),
					marker = $(this).data('marker'),
					markerTitle = $(this).data('marker-title'),
					styles = $(this).data('styles');
			$(this).height(mapHeight);
			$(this).gmap3({
          marker:{
            address: address,
            data: markerTitle,
            options: {
            	icon: marker
            },
            events: {
              mouseover: function(marker, event, context){
                var map = $(this).gmap3("get"),
                  	infowindow = $(this).gmap3({get:{name:"infowindow"}});
                if (infowindow){
                  infowindow.open(map, marker);
                  infowindow.setContent(context.data);
                } else {
                  $(this).gmap3({
                    infowindow:{
                      anchor:marker,
                      options:{content: context.data}
                    }
                  });
                }
              },
              mouseout: function(){
                var infowindow = $(this).gmap3({get:{name:"infowindow"}});
                if (infowindow){
                  infowindow.close();
                }
              }
            }
          },
          map:{
            options:{
              zoom: zoom,
              disableDefaultUI: controls,
              scrollwheel: scrollwheel,
              styles: styles
            }
          }
			});
		});
	}

});/*Document Ready End*/
//------------------------------------------------------------------------------
// Seacrh
$(document).ready(function () {
	var searchForm = $(".search-form");
	var searchInput = searchForm.find("[name='q']");
	// var typingTimer;
	// var typingInterval = 2000 ;
	// searchInput.keyup(function (event) {
	// 	// clearTimeout(typingInterval);
	// 	typingTimer = setTimeout(peformSearch, typingInterval);
	// });
	// searchInput.keydown(function (event) {
	// 	// clearTimeout(typingInterval);
	// });
	// searchInput.keypress(function (event) {
	// 	// clearTimeout(typingInterval);
	// });
	searchInput.blur(function(){
		peformSearch();
	});
	searchForm.submit(function(){
		peformSearch();
	});
	function peformSearch() {
		var query = searchInput.val();
		window.location.href='/timkiem/?q=' + query;
		
	}
});


