function show() {
    document.getElementById('rm1').className = 'show-div';
    document.getElementById('rm2').className = 'show-div';
    document.getElementById('rm3').className = 'show-div';
    document.getElementById('rm-link').className = 'hide-div';

}

function hide() {
    document.getElementById('rm1').className = 'hide-div';
    document.getElementById('rm2').className = 'hide-div';
    document.getElementById('rm3').className = 'hide-div';
    document.getElementById('rm-link').className = 'show-div';

}

var rm_link = document.getElementById('rm-link');
rm_link.onclick = show;

var rl_link = document.getElementById('rl-link');
rl_link.onclick = hide;

// var $ = jQuery.noConflict();

// $(document).ready(function() {
//     // add handler
//     $('#run-again').click(function() {
//         $('#words').prop('disabled', true);
//         $('#mixed').prop('disabled', true);
//         $('#numbers').prop('disabled', true);
//         $('#dice4').prop('disabled', true);
//         $('#dice5').prop('disabled', true);
//         $('#rolls3').prop('disabled', true);
//         $('#rolls4').prop('disabled', true);
//         $('#rolls5').prop('disabled', true);
//     });
// });


$(document).ready(function() {
    // add handler
    $('#mixed, #numbers').click(function() {

        $('#dice4').prop('disabled', true);
        $('#dice5').prop('disabled', true);
        $('#rolls3').prop('disabled', true);
        $('#rolls4').prop('disabled', true);
        $('#rolls5').prop('disabled', true);

        $('#length').val('20');
    });
});

$(document).ready(function() {

    $('#uuid').click(function() {

        $('#dice4').prop('disabled', true);
        $('#dice5').prop('disabled', true);
        $('#rolls3').prop('disabled', true);
        $('#rolls4').prop('disabled', true);
        $('#rolls5').prop('disabled', true);

        $('#length').val('32');
    });
});

// http://stackoverflow.com/questions/22581345/click-button-copy-to-clipboard-using-jquery
// function copyToClipboard(element) {

$(document).ready(function() {
    // add handler
    $('#copy-secret').click(function() {

        var $temp = $('<input>');
        $('body').append($temp);
        $temp.val($('#secret-field').text()).select();
        document.execCommand('copy');
        $temp.remove();
    });
});

// var $ = jQuery.noConflict();

$(document).ready(function() {
    // add handler
    $('#words').click(function() {

        // find all checked and cancel checked
        $('input:radio:checked').prop('disabled', false);

        // find all checked and cancel checked
        $('#dice4').prop('disabled', false);
        $('#dice5').prop('disabled', false);
        $('#rolls3').prop('disabled', false);
        $('#rolls4').prop('disabled', false);
        $('#rolls5').prop('disabled', false);

        // this radio add checked
        $('#dice5').prop('checked', true);
        $('#rolls5').prop('checked', true);
    });
});

$(document).ready(function() {
    $('#generate-btn, #run-again').click(function() {
        $('#spinner').show();
    });
});

// show/hide functionality on secret field
$(document).ready(function() {
    // add handler
    $('.toggler-icon').click(function() {
        $(this).toggleClass('fa-eye fa-eye-slash');
    });
});

// Keep tab selected on page refresh
// https://stackoverflow.com/questions/18999501/bootstrap-3-keep-selected-tab-on-page-refresh#19015027
$(document).ready(function() {
    if (location.hash) {
        $("a[href='" + location.hash + "']").tab('show');
    }
    $(document.body).on('click', 'a[data-toggle]', function(event) {
        location.hash = this.getAttribute("href");
    });

    $(window).on('popstate', function() {
        var anchor = location.hash ||
            $('a[data-toggle="tab"]').first().attr('href');
        $("a[href='" + anchor + "']").tab('show');
    });
});
