document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => {load_mailbox('inbox');sessionStorage.setItem('view', 'inbox')});
  document.querySelector('#sent').addEventListener('click', () => {load_mailbox('sent');sessionStorage.setItem('view', 'sent')});
  document.querySelector('#archived').addEventListener('click', () => {load_mailbox('archive');sessionStorage.setItem('view', 'archive')});
  document.querySelector('#compose').addEventListener('click', () => {compose_email() ; sessionStorage.setItem('view', 'compose_email')});

  // By default, load the inbox
  let view = sessionStorage.getItem('view');
  if (view === null){
    load_mailbox('inbox');
  } else {
    let view = sessionStorage.getItem('view');
    if (view === 'compose_email'){
      compose_email;
    } else {
      load_mailbox(view);
    }
  };

  //submit compose form
  document.querySelector("#compose-form").onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
      })
    .then(response => {
      console.log(response);
      response.json();
      })
    .then(result => {
        // Print result
        console.log(result);
      })
    .catch(error => {
      console.log('Error:', error);
      });
    sessionStorage.setItem('view', 'sent');
  };

  document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === 'archive col-2') {
      element.parentElement.style.animationPlayState = 'running';
      element.parentElement.addEventListener('animationend', () =>  {
        const elementParent = element.parentElement;
        const email_id = elementParent.querySelector('.email_id').innerHTML;
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: true
          })
        })
        window.location.reload();
      });
      } else if (element.className === 'unarchive col-2'){
        element.parentElement.style.animationPlayState = 'running';
        element.parentElement.addEventListener('animationend', () =>  {
          const elementParent = element.parentElement;
          const email_id = elementParent.querySelector('.email_id').innerHTML;
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false
            })
          })
          sessionStorage.setItem('view', 'inbox');
          window.location.reload();
        });
      }
  });

});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Load the mails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      // ... do something else with emails ...
      emails.forEach(email => {
        const mail = document.createElement('div');
        mail.className = "card";
        let contents = `<p class="email_id" hidden>${email['id']}</p> <h5>Subject: ${email['subject']}</h5>`
        let sender_or_receiver = `<h5>Sender: ${email['sender']}</h5>`;
        let button = `<button class="archive col-2">Archive</button>`;
        if (mailbox == 'sent'){
          sender_or_receiver = `<h5>recipients: ${email['recipients']}</h5>`;
          button = ``;
        };
        if (mailbox === 'archive'){
          button = `<button class="unarchive col-2"> Unarchive </button>`
        };
        contents = sender_or_receiver + contents + `<h6>Timestamp: ${email['timestamp']}</h6>`;
        mail.innerHTML = `${contents} ${button}`;
        document.querySelector('#emails-view').append(mail);
      });
  })
  .catch(error => {
    console.log('Error:', error);
  });

}