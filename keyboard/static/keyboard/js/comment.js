// import { getCookie } from './script.js' 


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