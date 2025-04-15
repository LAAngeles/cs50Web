document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('click', form_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function user_reply(email) {
  console.log(`user_reply ${email.id}`)
  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = email.recipients;
  document.querySelector('#compose-subject').value = email.subject;
  document.querySelector('#compose-body').value = `"${email.timestamp} ${email.sender} wrote: "${email.body}`;
}

function put_archived(email_id, archived_value){
  console.log(email_id);
  console.log(archived_value);

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archived_value,
    })
  })
  if (archived_value) {
    alert(`Email Archived`); 
  }else{
    alert(`Email Unarchived`); 
  }
  window.location.reload();
}

function put_email(email_id){
  console.log("put_email()");
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true,
    })
  }) 
}

function view_email(email_id) {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    document.querySelector('#email-view').innerHTML = `<h4>Content...</h4>`;
    // get access to API
    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Print email
      console.log(email);
      console.log(email.id);

      // ... do something else with email ...
      
      const boxOne = document.createElement('div');
      boxOne.innerHTML = `<strong>From:</strong> ${email.sender}`;
      document.querySelector('#email-view').append(boxOne);

      const boxTwo = document.createElement('div');
      boxTwo.innerHTML = `<strong>To:</strong> ${email.recipients}`;
      document.querySelector('#email-view').append(boxTwo);

      const boxThree = document.createElement('div');
      boxThree.innerHTML = `<strong>Subject:</strong> ${email.subject}`;
      document.querySelector('#email-view').append(boxThree);

      const boxFour = document.createElement('p');
      boxFour.innerHTML = `<strong>Timestamp:</strong> ${email.timestamp}`;
      document.querySelector('#email-view').append(boxFour);

    //////////////////////////////////////////////
    const checkBox = document.createElement('INPUT');
    checkBox.setAttribute("type", "button");
    checkBox.setAttribute("value", "Reply Email...");
    checkBox.classList.add('btn');
    checkBox.classList.add('btn-sm');
    checkBox.classList.add('btn-outline-primary');
    checkBox.addEventListener('click', function() {user_reply(email)});
    document.querySelector('#email-view').append(checkBox);
    //////////////////////////////////////////////

    const boxFive = document.createElement('p');
    boxFive.innerHTML = `<strong>Body:</strong> ${email.body}`;
    document.querySelector('#email-view').append(boxFive);  
  
      if (email.read == false) {
        put_email(email_id)
      }
 
    })
        // Catch any errors and log them to the console
    .catch(error => {
      console.log('Error:', error);
    });
}

function submit_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: 'bar@example.com',
        subject: 'Meeting time',
        body: 'How about we meet tomorrow at 3pm?'
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      // By default, load the inbox
      load_mailbox('sent');
  })
      // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
  });
}

function form_email(){

  const subject_form = document.querySelector('#compose-subject').value;
  const recipients_form = document.querySelector('#compose-recipients').value;
  const body_form = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients_form,
        subject: subject_form,
        body: body_form
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      // By default, load the sent
      load_mailbox('sent');
  })
      // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
  });
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'flex';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // get access to API
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      const heading = document.querySelector('h2');
  
      // ... do something else with emails ...
      switch(`${mailbox}`) {
        case 'inbox':
          // code block
          console.log("inbox")
          emails.forEach(item => {

            if (heading.innerHTML != item.sender) {

              const boxOne = document.createElement('div');
              boxOne.classList.add('sender');
              if (item.read == true) {boxOne.classList.add('gray');}
              boxOne.innerHTML = `${item.sender}`;
              ///////////////////////////////////////
              boxOne.addEventListener('click', function() {view_email(item.id)});
              ///////////////////////////////////////
              document.querySelector('#emails-view').append(boxOne);
              
              const boxTwo = document.createElement('div');
              boxTwo.classList.add('subject');
              if (item.read == true) {boxTwo.classList.add('gray');}
              boxTwo.innerHTML = `${item.subject}`;
              boxTwo.addEventListener('click', function() {view_email(item.id)});
              document.querySelector('#emails-view').append(boxTwo);

              const boxThree = document.createElement('div');
              boxThree.classList.add('timestamp');
              if (item.read == true) {boxThree.classList.add('gray');}
              boxThree.innerHTML = `${item.timestamp}`;
              boxThree.addEventListener('click', function() {view_email(item.id)});
              document.querySelector('#emails-view').append(boxThree);

              const checkBox = document.createElement('INPUT');
              checkBox.setAttribute("type", "button");
              checkBox.setAttribute("value", "Archive");
              checkBox.classList.add('btn');
              checkBox.classList.add('btn-sm');
              checkBox.classList.add('btn-outline-primary');
              checkBox.classList.add('archive');
              if (item.read == true) {checkBox.classList.add('gray');}
              checkBox.addEventListener('click', function() {put_archived(item.id, value=true)});
              document.querySelector('#emails-view').append(checkBox);

            }
          });
          break;
        case 'sent':
          // code block
          console.log("sent")
          emails.forEach(item => {
            item.recipients.forEach(recipient =>{

              const boxOne = document.createElement('div');
              boxOne.classList.add('sender');
              boxOne.innerHTML = `${recipient}`;
              document.querySelector('#emails-view').append(boxOne);

              const boxTwo = document.createElement('div');
              boxTwo.classList.add('subject');
              boxTwo.innerHTML = `${item.subject}`;
              document.querySelector('#emails-view').append(boxTwo);

              const boxThree = document.createElement('div');
              boxThree.classList.add('timestamp');
              boxThree.innerHTML = `${item.timestamp}`;
              document.querySelector('#emails-view').append(boxThree);
            });
          });
          break;
        case 'archive':
          // code block
          console.log("archive")


          ///////////////////////////////////
          emails.forEach(item => {

            if (heading.innerHTML != item.sender && item.archived == true) {

              const boxOne = document.createElement('div');
              boxOne.classList.add('sender');
              if (item.read == true) {boxOne.classList.add('gray');}
              boxOne.innerHTML = `${item.sender}`;
              ///////////////////////////////////////
              boxOne.addEventListener('click', function() {view_email(item.id)});
              ///////////////////////////////////////
              document.querySelector('#emails-view').append(boxOne);
              
              const boxTwo = document.createElement('div');
              boxTwo.classList.add('subject');
              if (item.read == true) {boxTwo.classList.add('gray');}
              boxTwo.innerHTML = `${item.subject}`;
              boxTwo.addEventListener('click', function() {view_email(item.id)});
              document.querySelector('#emails-view').append(boxTwo);

              const boxThree = document.createElement('div');
              boxThree.classList.add('timestamp');
              if (item.read == true) {boxThree.classList.add('gray');}
              boxThree.innerHTML = `${item.timestamp}`;
              boxThree.addEventListener('click', function() {view_email(item.id)});
              document.querySelector('#emails-view').append(boxThree);

              const checkBox = document.createElement('INPUT');
              checkBox.setAttribute("type", "button");
              checkBox.setAttribute("value", "Unarchived");
              checkBox.classList.add('btn');
              checkBox.classList.add('btn-sm');
              checkBox.classList.add('btn-outline-primary');
              if (item.read == true) {checkBox.classList.add('gray');}
              checkBox.addEventListener('click', function() {put_archived(item.id, value=false)});
              document.querySelector('#emails-view').append(checkBox);

            }
          });
          ///////////////////////////////////
          break;
        default:
          // code block
          console.log("switch")
      }
  })
      // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
  });
}