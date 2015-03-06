$(document).ready(function() {

    $("#applymodal").click(function() {
        var selectedCheckBoxList = [];
        selectedCheckBoxList = getCheckedIDUsingClass();
        $("#jobIDList").val(selectedCheckBoxList);
        $("#linkedinjobIDList").val(selectedCheckBoxList);
        console.log("Ok")
        console.log(selectedCheckBoxList)
        return (selectedCheckBoxList)
    });


    $('#toggle1').click(function() {
        $('.toggle1').toggle();
        return false;
    });

    // New JS functions to have onclick focus
    $("#titleedit").click(function() {
        $("#job_title").focus();
    });





    // Edit the Job Location details
    $('#locationedit').click(function() {
        var text = $('.job-location').text();
        text = $.trim(text);
        console.log(text);
        var input = $('<input id="job" class = "controls form-control col-md-12" value=" ' + text + '" /> ')
        console.log(input);
        $('.job-location').text('').append(input);
        input.select();

        input.blur(function() {
            var text = $('#attribute').val();
            $('#attribute').parent().text(text);
            $('#attribute').remove();
        });
    });


    // Edit the Job Status details
    $('#statusedit').click(function() {
        var text = $('.job-status').text();
        text = $.trim(text);
        console.log(text);
        var input = $('<input id="job" class = "controls form-control col-md-12" value=" ' + text + '" /> ')
        console.log(input)
        $('.job-status').text('').append(input);
        input.select();

        input.blur(function() {
            var text = $('#attribute').val();
            $('#attribute').parent().text(text);
            $('#attribute').remove();
        });
    });

    // Edit the Job Qualification details
    $('#qualificationedit').click(function() {
        var text = $('.job-qualification').text();
        text = $.trim(text);
        console.log(text);
        var input = $('<input id="job" class = "controls form-control col-md-12" value=" ' + text + '" /> ')
        console.log(input);
        $('.job-qualification').text('').append(input);
        input.select();

        input.blur(function() {
            var text = $('#attribute').val();
            $('#attribute').parent().text(text);
            $('#attribute').remove();
        });
    });



    // Edit the job type details
    $('#typeedit').click(function() {
        var text = $('.job-type').text();
        text = $.trim(text);
        console.log(text);
        var input = $('<input id="job" class = "controls form-control col-md-12" value=" ' + text + '" /> ')
        console.log(input)
        $('.job-type').text('').append(input);
        input.select();

        input.blur(function() {
            var text = $('#attribute').val();
            $('#attribute').parent().text(text);
            $('#attribute').remove();
        });
    });

    // Edit the Job experience details
    $('#experienceedit').click(function() {
        var text = $('.job-experience').text();
        text = $.trim(text);
        console.log(text);
        var input = $('<input id="job" class = "controls form-control col-md-12" value=" ' + text + '" /> ')
        console.log(input);
        $('.job-experience').text('').append(input);
        input.select();

        input.blur(function() {
            var text = $('#attribute').val();
            $('#attribute').parent().text(text);
            $('#attribute').remove();
        });
    });

    $('#checkmore').collapser({
        mode: 'chars',
        truncate: 30
    });



 function accordianDesc(IDofObject){
     $(IDofObject).collapser({
        mode: 'chars',
        truncate: 30
    });
}

    // Edit the Job institution details
    $('#institutionedit').click(function() {
        var text = $('.job-institution').text();
        text = $.trim(text);
        console.log(text);
        var input = $('<input id="job" class = "controls form-control col-md-12" value=" ' + text + '" /> ')
        console.log(input)
        $('.job-institution').text('').append(input);
        input.select();

        input.blur(function() {
            var text = $('#attribute').val();
            $('#attribute').parent().text(text);
            $('#attribute').remove();
        });
    });


});


// $(function() {
// // trying autocomplete
// $('#city').autocomplete({

//       source: function( request, response ) {
//         $.ajax({
//           url: "http://gd.geobytes.com/AutoCompleteCity",
//           dataType: "jsonp",
//           data: {
//             q: request.term
//           },
//           success: function( data ) {
//             response( data );
//           }
//         });
//       },
//       minLength: 3

//     });
// });

function getCheckedIDUsingClass() {
    / * declare an checkbox array * /
    var selectedCheckBoxList = [];
    // look
    //for all checkboxes that have a class 'chk'
    //attached to it and check
    //if it was checked //
    var chkId = "";
    $('.chk:checked').each(function() {
        chkId += $(this).val() + ", ";
    });

    chkId = chkId.slice(0, -1);
    // check
    // if there is selected checkboxes, by
    // default the length is 1 as it contains one single comma

    if (chkId.length > 1) {
        //
        //alert("You have selected # " + chkId + "Jobs ");
        // } else {
        //     alert("Please check atleast one checkbox to apply for the Jobs ");
        // }
        return (chkId)
    }
}