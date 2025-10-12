document.addEventListener("DOMContentLoaded", function () {
    // Check if Google Maps API is loaded, if not wait for it
    if (typeof google !== 'undefined' && google.maps) {
        initAutoComplete();
    } else {
        // Wait for Google Maps to load
        window.initMap = function() {
            initAutoComplete();
        };
    }
});

let autocomplete;

function initAutoComplete(){
    // Add a check to ensure google is available
    if (typeof google === 'undefined' || !google.maps) {
        console.error('Google Maps API not loaded');
        return;
    }
    
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: {'country': ['in']},
        })
    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }

    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value
    geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var lat = results[0].geometry.location.lat();
            var lng = results[0].geometry.location.lng();
            $('#id_latitude').val(lat)
            $('#id_longitude').val(lng)
            $('#id_address').val(address)
        }
    })
    for (var i = 0; i < place.address_components.length; i++) {
        for (var j = 0; j < place.address_components[i].types.length; j++) {
            // get country
            if (place.address_components[i].types[j] == "country") {
                $('#id_country').val(place.address_components[i].long_name)
            }
            // get state
            if (place.address_components[i].types[j] == "administrative_area_level_1") {    
                $('#id_state').val(place.address_components[i].long_name)
            }
            // get city
            if (place.address_components[i].types[j] == "administrative_area_level_3") {
                $('#id_city').val(place.address_components[i].long_name)
            }
            // get pincode
            if (place.address_components[i].types[j] == "postal_code") {
                $('#id_pin_code').val(place.address_components[i].long_name)
            }
            else{
                $('#id_pin_code').val('')

            }
        }
    }
}

$(document).ready(function(){
    $('.add-to-cart').on('click', function(e){
        e.preventDefault();
        var foodId = $(this).data('id');
        url = $(this).data('url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if (response.status == 'Success'){
                $('#cart-count').html(response.cart_count['cart_count'])
                $('#qty_' + foodId).html(response.qty)
                // subtotal, tax, grand_total
                applyCartAmount(response.cart_amount['sub_total'], response.cart_amount['tax'], response.cart_amount['grand_total'])
                }
                else if(response.status == 'login_required'){
                    swal( response.message, "Please login to continue", "info").then(function(){
                        window.location.href = "/login";
                    })
                }
                else{
                    swal(response.message, '', 'error')
                }
            }
        })
    })
    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#' + the_id).html(qty)
    })

$('.remove-from-cart').on('click', function(e){
        e.preventDefault();
        var foodId = $(this).data('id');
        url = $(this).data('url');
        var cartId = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
            if (response.status == 'Success'){
                $('#cart-count').html(response.cart_count['cart_count'])
                $('#qty_' + foodId).html(response.qty)
                removeCartItem(response.qty, cartId);
                checkEmptyCart();
                // sub_total, tax, grand_total
                applyCartAmount(response.cart_amount['sub_total'], response.cart_amount['tax'], response.cart_amount['grand_total'])
            }
            else if(response.status == 'login_required'){
                swal( response.message, "Please login to continue", "info").then(function(){
                    window.location.href = "/login";
                })
            }
            else{
                swal(response.message, '', 'error')
            }
        }
    })
    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#' + the_id).html(qty)
    })
})


$('.delete-cart').on('click', function(e){
        e.preventDefault();
        var cart = $(this).data('id');
        url = $(this).data('url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
            if (response.status == 'Success'){
                $('#cart-count').html(response.cart_count['cart_count'])
                swal(response.status, response.message, "success")
                removeCartItem(0, cart);
                checkEmptyCart();
                applyCartAmount(response.cart_amount['sub_total'], response.cart_amount['tax'], response.cart_amount['grand_total'])
            }
            else{
                swal(response.status, response.message, 'error')
            }
        }
    })
})

    // delete the cart element if the quantity is 0
    function removeCartItem(qty, cartId){
        if(window.location.pathname == '/cart/'){
            if(qty <= 0){
                $('#cart-item-' + cartId).remove();
            }
        }
    }
    function checkEmptyCart(){
        var cartCount = document.getElementById('cart-count').innerHTML;
        if(cartCount == 0){
            $('#empty-cart').show();
        }
    }

    function applyCartAmount(sub_total, tax, grand_total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(sub_total)
            $('#tax').html(tax)
            $('#total').html(grand_total)
    }
}

$('.add_opening_hour').on('click', function(e){
    e.preventDefault();
    var day = $('#id_day').val();
    var from_hour = $('#id_from_hour').val();
    var to_hour = $('#id_to_hour').val();
    var is_closed = $('#id_is_closed').is(':checked') ? true : false;
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var url = $('#url_id').val();
    console.log(day, from_hour, to_hour, is_closed, csrf_token);
    if(day == '' || (from_hour == '' && !is_closed) || (to_hour == '' && !is_closed)){
        swal('Please fill all the fields', '', 'info')
        return false;
    }
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'day': day,
            'from_hour': from_hour,
            'to_hour': to_hour,
            'is_closed': is_closed,
            'csrfmiddlewaretoken': csrf_token
        },
        success: function(response){
            if(response.status == 'Success'){
                swal(response.status, response.message, "success").then(function(){
                    html ='<tr id="hour_' + response.id + '"><td>' + response.day + '</td><td>' + (response.is_closed ? 'Closed' : response.from_hour + ' - ' + response.to_hour) + '</td><td><a href="#" class="btn btn-sm btn-danger remove_opening_hour" data-id="' + response.id + '" data-url="/vendor/opening-hours/delete/' + response.id + '">Delete</a></td></tr>';
                    $('#opening_hours_table').append(html);
                    $('#opening_hours_form')[0].reset();
                });
            }
            else{
                swal(response.status, response.message, "error");
            }
        }
    })

})

$(document).on('click', '.remove_opening_hour', function(e){
    e.preventDefault();
    url = $(this).data('url');
    console.log(url);

    $.ajax({
        type: 'GET',
        url: url,
        success: function(response){
            if(response.status == 'Success'){
                swal(response.status, response.message, "success").then(function(){
                    console.log('#hour_' + response.id);
                    $('#hour_' + response.id).remove();
                });
            }
            else{
                swal(response.status, response.message, "error");
            }
        }
    })

})

// end of document.ready function
})
