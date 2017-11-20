// General JavaScript functions and scripts for site functionality

function show_content() {
    document.getElementById('rm1').className = 'show';
    document.getElementById('rm2').className = 'show';
    document.getElementById('rm3').className = 'show';
    document.getElementById('rm-link').className = 'hide';

}

function hide_content() {
    document.getElementById('rm1').className = 'hide';
    document.getElementById('rm2').className = 'hide';
    document.getElementById('rm3').className = 'hide';
    document.getElementById('rm-link').className = 'show';

}

var rm_link = document.getElementById('rm-link');
var rl_link = document.getElementById('rl-link');

rl_link.onclick = hide_content;
rm_link.onclick = show_content;

var $js = jQuery.noConflict();

// $js(document).ready(function() {
//     // add handler
//     $js('#run-again').click(function() {
//         $js('#words').prop('disabled', true);
//         $js('#mixed').prop('disabled', true);
//         $js('#numbers').prop('disabled', true);
//         $js('#dice4').prop('disabled', true);
//         $js('#dice5').prop('disabled', true);
//         $js('#rolls3').prop('disabled', true);
//         $js('#rolls4').prop('disabled', true);
//         $js('#rolls5').prop('disabled', true);
//     });
// });

$js(document).ready(function() {
    // add handler
    $js('#mixed, #numbers').click(function() {

        $js('#dice4').prop('disabled', true);
        $js('#dice5').prop('disabled', true);
        $js('#rolls3').prop('disabled', true);
        $js('#rolls4').prop('disabled', true);
        $js('#rolls5').prop('disabled', true);

        $js('#length').val('20');
    });
});

$js(document).ready(function() {

    $js('#uuid').click(function() {

        $js('#dice4').prop('disabled', true);
        $js('#dice5').prop('disabled', true);
        $js('#rolls3').prop('disabled', true);
        $js('#rolls4').prop('disabled', true);
        $js('#rolls5').prop('disabled', true);

        $js('#length').val('32');
    });
});

// http://stackoverflow.com/questions/22581345/click-button-copy-to-clipboard-using-jquery
// function copyToClipboard(element) {

$js(document).ready(function() {
    // add handler
    $js('#copy-secret').click(function() {

        var $jstemp = $js('<input>');
        $js('body').append($jstemp);
        $jstemp.val($js('#secret-field').text()).select();
        document.execCommand('copy');
        $jstemp.remove();
    });
});

$js(document).ready(function() {
    // add handler
    $js('#words').click(function() {

        var dice5 = $js('#dice5');
        var rolls5 =  $js('#rolls5');

        // find all checked and cancel checked
        $js('input:radio:checked').prop('disabled', false);

        // find all checked and cancel checked
        $js('#dice4').prop('disabled', false);
        dice5.prop('disabled', false);
        $js('#rolls3').prop('disabled', false);
        $js('#rolls4').prop('disabled', false);
        rolls5.prop('disabled', false);

        // this radio add checked
        dice5.prop('checked', true);
        rolls5.prop('checked', true);
    });
});

$js(document).ready(function() {
    $js('#generate-btn, #run-again').click(function() {
        $js('#spinner').show();
    });
});

// show/hide functionality on secret field
$js(document).ready(function() {
    // add handler
    $js('.toggler-icon').click(function() {
        $js(this).toggleClass('fa-eye fa-eye-slash');
    });
});

// Keep tab selected on page refresh
// https://stackoverflow.com/questions/18999501/bootstrap-3-keep-selected-tab-on-page-refresh#19015027
$js(document).ready(function() {
    if (location.hash) {
        $js("a[href='" + location.hash + "']").tab('show');
    }
    $js(document.body).on('click', 'a[data-toggle]', function(event) {
        location.hash = this.getAttribute("href");
    });

    $js(window).on('popstate', function() {
        var anchor = location.hash ||
            $js('a[data-toggle="tab"]').first().attr('href');
        $js("a[href='" + anchor + "']").tab('show');
    });
});
