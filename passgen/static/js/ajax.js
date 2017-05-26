
// attempt to explore AJAX post
//
// $.ajax({
//     type: "POST",
//     url: '/generate',
//     data: { output_type: "mixed" },
//     success: 'success'
// });

$(document).ready(function() {

    $('#run-again').click(function(e) {
        e.preventDefault();

        var data = {
            number_roll: output_type,
            number_dice: '5',
            how_many: '1',
            output_type: 'mixed',
            password_length: '10'
        };

        $.ajax({
            type: 'post',
            url: '/generate',
            data: data,
            success: 'success',
            error: 'error'
        }).done(function() {
            console.log('sent');
        });
    });
});