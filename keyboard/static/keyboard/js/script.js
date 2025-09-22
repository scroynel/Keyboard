// Slider for items in delail view
new Swiper('.carousel-detail', {
  loop: true,

  // Paginations dots
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
    dynamicBullets: true

  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function toggleCart() {
  const $cart = $('#cart');
  const $overlay = $('#cart-slide');

  if ($cart.css('right') === '0px') {
    // Close cart
    $overlay.removeClass('bg-opacity-50').addClass('bg-opacity-0')
    $cart.removeClass('right-0').addClass('right-[-100%]')
    $('body').removeClass('overflow-hidden');
    setTimeout(() => {
      $overlay.addClass('hidden');
    }, 300)
  } else {
    // Open cart
    $overlay.removeClass('hidden');
    void $overlay[0].offsetWidth; // That transition works well
    $overlay.removeClass('bg-opacity-0').addClass('bg-opacity-50');
    $cart.removeClass('right-[-100%]').addClass('right-0');
    $('body').addClass('overflow-hidden');
  }
}

// Modal cart
$(document).ready(function() {
  $('#cart-button').on('click', function(e) {;
    toggleCart();
  })

  $('#cart-slide').on('click', function(e) {
    toggleCart();
  })

  $('#cart').on('click', function(e) {
    e.stopPropagation();
  })

  $('#cart').on('click', '.button-modal', function(e) {
    toggleCart();
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
      toggleCart();
    },
    error: (error) => {
      console.log(error);
    }
  })
})


// Delete-link ajax (without refresh page) for cart
$('#cart').on('click', '.delete-link', function(e) {
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


$('#comment_form_submit').on('submit', function(e) {
  e.preventDefault();
  form = $('#comment_form_submit');
  action_url = form.attr('data-href')
  $.ajax({
    url: action_url,
    type: 'POST',
    dataType: 'json',
    accepts: 'application/json',
    data: form.serialize(),
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"), // function to get coookie by name 
    },
    success: (data) => {
      $("#comment_list").html(data.comment_list);
      $('#avg_rating').text(data.avg_rating)
      $('#comments_count').text(data.comments_count + ' replies')
    },
    error: (error) => console.log(error)
  });
})


$('.likes').on('click', '.wishlist', function(e) {
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
      if (data.status === 'added') {
        $(this).addClass('active')
      } else if (data.status === 'removed') {
        $(this).removeClass('active')
      }
    },
    error: (error) => {
      console.log(error);
    }
  })
})


$('#content').on('click', '.wishlistdel', function(e) {
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
      if (data.status === 'removed') {
        $(this).removeClass('active')
        $(this).closest('.wishlist-user').fadeOut()
        console.log(data.count)
        if (data.count == 0){
          $('#content').html(data.wishlist_empty)
        }
      }
    },
    error: (error) => {
      console.log(error);
    }
  })
})