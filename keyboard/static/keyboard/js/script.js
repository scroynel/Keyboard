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


// Modal cart
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




// Delete-link ajax (without refresh page) for cart
$('.delete-link').on('click', function(e) {
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
          let code = `
            <div id="cart-empty" class="w-full h-full flex justify-center items-center">
              <div class="text-center">
                  <p class="text-4xl">Your cart is empty</p>
                  <button id="button-modal" type="button" class="inline-block border-4 hover:border-gray-400 hover:shadow-md shadow-black mt-10 p-4">Continue shopping</button>
                  <p class="text-2xl mt-10">Have an account?</p>
                  <p><a id="login" href="${login}" class="underline text-xl">Log in</a> to check out faster.</p>
              </div>
          </div>
          `
          $('#cart').html(code)
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


$('#qty').on('change', function(e) {
  e.preventDefault();
  qty = $('#qty').val()
  update_url = $('#qty').attr('data-href')
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