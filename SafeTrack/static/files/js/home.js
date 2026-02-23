// Simple scroll reveal (optional)
$(window).on("scroll", function () {
    $(".fade-in").each(function () {
        let top = $(this).offset().top;
        let scroll = $(window).scrollTop() + window.innerHeight - 100;
        if (scroll > top) {
            $(this).addClass("visible");
        }
    });
});
