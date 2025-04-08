
document.addEventListener("DOMContentLoaded", function () {
    initAutoComplete();
});

let autocomplete;

function initAutoComplete(){
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
})
