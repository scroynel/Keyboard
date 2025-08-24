// import { getCookie } from "./script.js";


$(document).ready(function() {
  $('#cart-button').on('click', function(e) {;
    $('#cart-slide').removeClass('hidden');
    $('body').addClass('overflow-hidden')
  })

  $('#cart-slide').on('click', function(e) {
    $('#cart-slide').addClass('hidden');
    $('body').removeClass('overflow-hidden')
  })

  $('#cart').on('click', function(e) {
    e.stopPropagation();
  })

  $('#button-modal').on('click', function(e) {
    $('#cart-slide').addClass('hidden')
  })
})


$('#add_to_cart').on('click', function(e) {
  e.preventDefault();
  $.ajax({
    url: $(this).attr('href'),
    type: 'POST',
    dataType: 'json',
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"), // function to get coookie by name 
    },
    success: (data) => {
      $('#cart').html(data.cart_list)
      $('#cart-slide').removeClass('hidden');
      $('body').addClass('overflow-hidden');
    },
    error: (error) => {
      console.log(error);
    }
  })
})


// Delete-link ajax (without refresh page) for cart
$('#cart').on('click', '.delete-link', function(e) {
// $(document).on('click', '.delete-link', function(e) {
  e.preventDefault();
  var login = 'login/' // It's a temporary solution #important
  $.ajax({
    url: $(this).attr('href'),
    type: "POST",
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"), // function to get coookie by name 
    },
    success: (data) => {
      if (data.status == 1) {
        $(this).closest('.cart-item').fadeOut();
        $('#total').text(data.total)
        if (data.count == 0) {
          $('#cart').html(data.empty_cart)
          $('#button-modal').on('click', function(e) {
            $('#cart-slide').addClass('hidden');
          })
        }
      }
    },
    error: (error) => {
      console.log(error);
    }
  })
})


$('#cart').on('change', 'input[id=qty]', function(e) {
  e.preventDefault();
  qty = $(this).val()
  update_url = $(this).attr('data-href')
  $.ajax({
    url: update_url,
    type: "POST",
    dataType: "json",
    data: {
      'qty': qty
    },
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"), // function to get coookie by name 
    },
    success: (data) => {
      console.log('data', data)
      if (data.status == 1) {
        $('#total').text(data.total)
      }
    },
    error: (error) => {
      console.log(error);
    }
  })
})