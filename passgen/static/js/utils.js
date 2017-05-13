function show() {
    document.getElementById('rm1').className = 'show-div';
    document.getElementById('rm2').className = 'show-div';
    document.getElementById('rm-link').className = 'hide-div';

}
function hide() {
    document.getElementById('rm1').className = 'hide-div';
    document.getElementById('rm2').className = 'hide-div';
    document.getElementById('rm-link').className = 'show-div';

}

var rm_link = document.getElementById('rm-link');
rm_link.onclick = show;

var rl_link = document.getElementById('rl-link');
rl_link.onclick = hide;

// var $ = jQuery.noConflict();

$(document).ready(function() {
    // add handler
    $('#mixed, #numbers').click(function(){

        // find all checked and cancel checked
        $('#dice4').prop('disabled', true);
        $('#dice5').prop('disabled', true);
        $('#rolls3').prop('disabled', true);
        $('#rolls4').prop('disabled', true);
        $('#rolls5').prop('disabled', true);

        if ($('#length').val() === '') {
            $('#length').val('20');
        }
    });
});

// http://stackoverflow.com/questions/22581345/click-button-copy-to-clipboard-using-jquery
// function copyToClipboard(element) {

$(document).ready(function() {
    // add handler
    $('#p2').click(function() {

        var $temp = $('<input>');
        $('body').append($temp);
        $temp.val($('#p1').text()).select();
        document.execCommand('copy');
        $temp.remove();
    });
});

// var $ = jQuery.noConflict();

$(document).ready(function() {
    // add handler
    $('#words').click(function(){

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
    $('#generate').click(function() {
        $('#spinner').show();
    });
});
