
    $(document).ready(function() {
     
      $("#owl-demo1").owlCarousel({
          autoPlay: 5000, navigation : false, pagination : false,
          items : 4,itemsDesktop : [1199,4],itemsDesktopSmall : [990,3],itemsTablet: [768,3],itemsMobile: [767,2],
      });
	  $("#owl-demo2").owlCarousel({
          autoPlay: 5000, navigation : true, pagination : false,
          items : 4,itemsDesktop : [1199,4],itemsDesktopSmall : [990,3],itemsTablet: [768,3],
      });
	  
	  $("#owl-demo3").owlCarousel({
          autoPlay: 5000, navigation : true, pagination : false,
          items : 4,itemsDesktop : [1199,4],itemsDesktopSmall : [990,3],itemsTablet: [768,3],
      });
	  
	  $("#owl-demo4").owlCarousel({
          autoPlay: 5000, navigation : false, pagination : true,
          items : 1,itemsDesktop : [1199,1],itemsDesktopSmall : [990,1],itemsTablet: [768,1],
      });

    });