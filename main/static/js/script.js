
$(document).ready(function () {
    
    // Modal confirmation of order
    $('#order-modal-btn').on("click", function () {
        $('#order-modal').modal("show");
        var storageUnit = $("#id_storage_unit option:selected").text();
        var startDate = $("#id_start_date").val();
        $('#order-modal-body').html(
            "<b>Storage unit: </b>" + storageUnit + "<br><b>Start date:</b> " + startDate
        );
    });

    $('.close-modal').on("click", function () {
        $('#order-modal').modal("hide");
    });

    // Create date for copyright footer
    $("#copyright").text(new Date().getFullYear());

    // Remove messages after 5 seconds
    setTimeout(function () {
        if ($('.alert').length > 0) {
            $('.alert').slideUp('100');
        }
    }, 5000);

    // Set aria-labels for form input elements
    $('#id_name').attr('aria-label', 'Enter name here');
    $('#id_email').attr('aria-label', 'Enter email here');
    $('#id_message').attr('aria-label', 'Enter message here');
    $('#id_storage_unit').attr('aria-label', 'Pick a storage unit');
    $('#id_start_date').attr('aria-label', 'Pick a start date');

    // Hide form error div if it has no content
    $('.help-block:empty').hide();

});

