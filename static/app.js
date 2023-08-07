$(document).ready(function() {
    // Handle dark mode and light mode switch
    $('#darkModeSwitch').change(function() {
        if ($(this).prop('checked')) {
            $('body').addClass('dark-mode');
        } else {
            $('body').removeClass('dark-mode');
        }
    });
});