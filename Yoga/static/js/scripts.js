
    (function($) {
  "use strict";

  $('[data-toggle="tooltip"]').tooltip();

  $('[data-toggle="popover"]').popover();

  $(".popover-dismiss").popover({
    trigger: "focus"
  });

  var path = window.location.href; 
  $("#layoutSidenav_nav .sidenav a.nav-link").each(function() {
    if (this.href === path) {
      $(this).addClass("active");
    }
  });

  $("#sidebarToggle").on("click", function(e) {
    e.preventDefault();
    $("body").toggleClass("sidenav-toggled");
  });

  feather.replace();

  $("body").scrollspy({
    target: "#stickyNav",
    offset: 82
  });

  $('.nav-sticky a.nav-link[href*="#"]:not([href="#"])').click(function() {
    if (
      location.pathname.replace(/^\//, "") ==
        this.pathname.replace(/^\//, "") &&
      location.hostname == this.hostname
    ) {
      var target = $(this.hash);
      target = target.length ? target : $("[name=" + this.hash.slice(1) + "]");
      if (target.length) {
        $("html, body").animate(
          {
            scrollTop: target.offset().top - 81
          },
          200
        );
        return false;
      }
    }
  });

  $("#layoutSidenav_content").click(function() {
    const BOOTSTRAP_LG_WIDTH = 992;
    if (window.innerWidth >= 992) {
      return;
    }
    if ($("body").hasClass("sidenav-toggled")) {
        $("body").toggleClass("sidenav-toggled");
    }
  });

  let activatedPath = window.location.pathname.match(/([\w-]+\.html)/, '$1');

  if (activatedPath) {
    activatedPath = activatedPath[0];
  }
  else {
    activatedPath = 'index.html';
  }
    
  let targetAnchor = $('[href="' + activatedPath + '"]');
  let collapseAncestors = targetAnchor.parents('.collapse');
  
  targetAnchor.addClass('active');
  
  collapseAncestors.each(function() {
    $(this).addClass('show');
    $('[data-target="#' + this.id +  '"]').removeClass('collapsed');
     
  })

})(jQuery);
