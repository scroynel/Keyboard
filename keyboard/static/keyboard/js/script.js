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


// Delete-link ajax (without refresh page)
$('.delete-link').on('click', function(e) {
  e.preventDefault()
  $.ajax({
    url: $(this).attr('href'),
    type: "POST",
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
    },
    success: (data) => {
      console.log('jsdglsgl');
      if (data.status == 1) {
        $(this).parent().parent().remove();
        $('#total').text(data.total)
        console.log(data.cart_products_user.length)
        if (data.cart_products_user.length == 0) {
          // $('#cart-not-empty').addClass('hidden')
          // $('#cart').html('<div class="w-full h-full flex justify-center items-center"><div class="text-center"><p class="text-4xl">Your cart is empty</p><button type="button" class="inline-block border-4 hover:border-gray-400 hover:shadow-md shadow-black mt-10 p-4" data-modal-hide="cart-slide">Continue shopping</button><p class="text-2xl mt-10">Have an account?</p><p><a href="#" class="underline text-xl">Log in</a> to check out faster.</p></div></div>')
        }
      }
      
    },
    error: (error) => {
      console.log(error);
    }
  })
})
