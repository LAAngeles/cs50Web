document.addEventListener('DOMContentLoaded', function() {
    // If hide button is clicked, delete the post
    document.addEventListener('click', event => {
        // Find what was clicked on
        const element = event.target;
        console.log(element)
        switch (element.id) {
            case "Next":        Next();                             break;
            case "Previous":    Previous();                         break;
            case "Like":        Like(element.dataset.post_id);      break;
            case "UnLike":      unLike(element.dataset.post_id);    break;
            case "edit_post":   Edit_Post(element.dataset.edit);    break;
            default: break;
        }
    });
    ActivateButton()
});

function ActivateButton() {
    console.log("ActivateButton()")
    unlikes = document.querySelectorAll('#UnLike');
    // document.querySelector('#Like').style.display = 'none';
    likes = document.querySelectorAll('#Like');

    unlikes.forEach(item =>{
        likes.forEach(element =>{
            if (`${element.dataset.post_id}` === `${item.dataset.post_id}`) {
                element.style.display = 'none';
            }
        });
    });
}

function Edit_Post(post_id) {
    console.log("case: Edit_Post");
    console.log(post_id);

    // Show the mailbox and hide other views
    posts = document.querySelectorAll('#edit_post')
    posts.forEach(item =>{
        if (`${post_id}` === `${item.dataset.edit}`) {
            item.style.display = 'none';
        }
    });
    // document.querySelector('#edit_post').style.display = 'none';
    ps = document.querySelectorAll('.pHide')
    ps.forEach(item =>{
        if (`${post_id}` === `${item.accessKey}`) {
            item.style.display = 'none';
        }
    });
    // document.querySelector('#edit_form').style.display = 'block';
    forms = document.querySelectorAll('#edit_form')
    forms.forEach(item =>{
        if (`${post_id}` === `${item.accessKey}`) {
            item.style.display = 'block';
        }
    });
    
    // document.querySelector('#edit_title').value = document.querySelector('#valueTitle').textContent;
    valoes = document.querySelectorAll('#valueTitle')
    edit_titles = document.querySelectorAll('#edit_title')
    valoes.forEach(item =>{
        console.log("item "+item.textContent )
        if (`${post_id}` === `${item.accessKey}`) {
            // document.querySelector('#edit_title').value = item.textContent;
            edit_titles.forEach(element =>{
                element.value = item.textContent;
            })
        }
    });
    // document.querySelector('#edit_body').value = document.querySelector('#valueContent').textContent;
    valoes = document.querySelectorAll('#valueContent')
    edit_bodies = document.querySelectorAll('#edit_body')
    valoes.forEach(item =>{
        console.log("item "+item.textContent )
        if (`${post_id}` === `${item.accessKey}`) {
            // document.querySelector('#edit_title').value = item.textContent;
            edit_bodies.forEach(element =>{
                element.value = item.textContent;
            })
        }
    });

    // document.querySelector('#id_pk').value = document.querySelector('#pk').textContent;
    pks = document.querySelectorAll('#pk')
    id_pks = document.querySelectorAll('#id_pk')
    pks.forEach(item =>{
        console.log("item "+item.textContent )
        if (`${post_id}` === `${item.accessKey}`) {
            // document.querySelector('#edit_title').value = item.textContent;
            id_pks.forEach(element =>{
                element.value = item.textContent;
            })
        }
    });
}

function Like(post_id) {
    
    const user_id = document.querySelector('#post-user_id').textContent;
    const likeUnlike = document.querySelector('#Like').value;
    console.log(likeUnlike)
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            user: user_id,
            post_id: post_id,
            likeUnlike: likeUnlike
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result

        //   document.querySelector('#Like').textContent = "UnLike";
        //   document.querySelector('#Like').id = "UnLike";
        //   document.querySelector('#UnLike').value = "False";

        posts = document.querySelectorAll('#Like')
        
        posts.forEach(item =>{
            if (`${post_id}` === `${item.dataset.post_id}`) {
                item.textContent = "UnLike";
                item.id = "UnLike";
                item.value = "False";
            }
        });
        // plusLike
        // document.querySelector('.plusLike').textContent = result["num_likes"];
        likes = document.querySelectorAll('.plusLike')
        likes.forEach(item =>{
            if (`${post_id}` === `${item.accessKey}`) {
                item.textContent = `${result["num_likes"]}`;
            }
        });

    }).catch(error => {console.log('Error:', error);});
}

function unLike(post_id) {
    
    const user_id = document.querySelector('#post-user_id').textContent;
    const likeUnlike = document.querySelector('#UnLike').value;
    console.log(likeUnlike)
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            user: user_id,
            post_id: post_id,
            likeUnlike: likeUnlike
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
        //   document.querySelector('#UnLike').textContent = "Like";
        //   document.querySelector('#UnLike').id = "Like";
        //   document.querySelector('#Like').value = "True";

          posts = document.querySelectorAll('#UnLike')

          posts.forEach(item =>{
              if (`${post_id}` === `${item.dataset.post_id}`) {
                  item.textContent = "Like";
                  item.id = "Like";
                  item.value = "True";
              }
          });
        //   document.querySelector('.plusLike').textContent = result["num_likes"];
        likes = document.querySelectorAll('.plusLike')
        likes.forEach(item =>{
            if (`${post_id}` === `${item.accessKey}`) {
                item.textContent = `${result["num_likes"]}`;
            }
        });
    }).catch(error => {console.log('Error:', error);});
      
}

function Next(params) {
    console.log("case: Next");
    // Show the mailbox and hide other views
    document.querySelector('#index-AllPost').style.display = 'none';
    document.querySelector('#index-Next').style.display = 'block';

    pageTwo()
}

function Previous() {
    document.querySelector('#index-AllPost').style.display = 'block';
    document.querySelector('#index-Next').style.display = 'none';
}

function pageTwo() {
    document.querySelector('#page-1').innerHTML = ``;
    fetch('/indexPage')
    .then(response => response.json())
    .then(posts => {
        // Print posts
        console.log(posts);

        // ... do something ...
        posts.forEach(element => {
            const boxPost = document.createElement('div')
            boxPost.className = "postDiv";
            boxPost.innerHTML = `<a href="/profile/${element.user_id}"><p>${element.user}</p></a>
                                <p>${element.title}</p>
                                <p>${element.body}</p>
                                <p>${element.timestamp}</p>
                                <i class="material-icons" style="font-size:16px;color:red;">favorite</i>
                                <p>${element.num_likes}</p>
                                <button id="Like"  class="btn btn-sm btn-outline-primary"  data-post_id = ${element.id} value="True">Like</button>`;
            document.querySelector('#page-1').append(boxPost);
        });

        const boxButton = document.createElement('div');
        boxButton.className = "";
        boxButton.innerHTML = `<button id="Previous" class="btn btn-primary" >Previous</button>`;
        document.querySelector('#page-1').append(boxButton);
    }).catch(error => {console.log('Error:', error);});
}