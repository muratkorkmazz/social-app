document.addEventListener('DOMContentLoaded', function() {
  
  
  document.querySelectorAll('.like_unlike_button').forEach(item => {
    

    item.addEventListener('click', (event)=>{
      let post_id = parseInt(event.target.id);
      let user_id = parseInt(document.querySelector('#user_id').innerHTML);
      let count_element = document.querySelector(`#total_likes_${post_id}`);
      let like_text_element = document.querySelector(`#like_text_${post_id}`)
      let count_value = parseInt(count_element.innerHTML);
      
      //console.log(count);
      //console.log(event.target.id);
      if(event.target.innerHTML === '❤️'){
        event.target.innerHTML = '🤍';
        count_element.innerHTML = count_value - 1;        
      }
      else{
        event.target.innerHTML = '❤️';
        count_element.innerHTML = count_value + 1;
      }

      if(parseInt(count_element.innerHTML) === 1){
        like_text_element.innerHTML = 'like'
      }
      else{
        like_text_element.innerHTML = 'likes';
      }

      fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            user_id: user_id
        })
      })
      .then(()=>console.log('success'))
      .catch(() => console.log('failed'));
    })
  })

  document.querySelectorAll('.edit-button').forEach(item => {
    item.addEventListener('click',(event)=>{
      
      let post_id = event.target.id.slice(1);
      //console.log(`trying to edit post ${post_id}`);
      let current_text = document.querySelector(`#post_content_${post_id}`).innerHTML.trim();
      //console.log(current_text);
      document.querySelector(`#show_post_${post_id}`).style.display = 'none';
      document.querySelector(`#edit_post_${post_id}`).style.display = 'block';
      document.querySelector(`#edit_post_content_${post_id}`).value = current_text;      
    })
  });

  
  document.querySelectorAll('.save_edit_button').forEach(item => {
    item.addEventListener('click', (event)=>{
      let post_id = event.target.id.slice(2);      
      let new_content = document.querySelector(`#edit_post_content_${post_id}`).value.trim();

      fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            new_content: new_content
        })
      })
      

      document.querySelector(`#show_post_${post_id}`).style.display = 'block';
      document.querySelector(`#edit_post_${post_id}`).style.display = 'none';
      document.querySelector(`#post_content_${post_id}`).innerHTML = new_content;
      
    })
  });

  if(document.querySelector('#follow-unfollow-button') !== null){
    document.querySelector('#follow-unfollow-button').addEventListener('click', (event)=>{
      let member_id = parseInt(document.querySelector('#member_id').innerHTML);
      let user_id = parseInt(document.querySelector('#user_id').innerHTML);
      //console.log(`${user_id} wants to follow ${member_id}`);
      let x = parseInt(document.querySelector('#follower_count').innerHTML);
      if(event.target.innerHTML == "Follow"){
        event.target.innerHTML = "Unfollow";
        event.target.className = "btn btn-warning";
        document.querySelector('#follower_count').innerHTML = x + 1;
      }
      else{
        event.target.innerHTML = "Follow";
        event.target.className = "btn btn-success";
        document.querySelector('#follower_count').innerHTML = x - 1;
      }     
      
      fetch(`/add_remove_follower/${member_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            follower_id: user_id
        })
      })
      

    });
  }
  
});