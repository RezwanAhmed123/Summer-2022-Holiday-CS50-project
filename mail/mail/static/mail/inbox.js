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
      return response.json;
      })
    .then(result => {
        // Print result
        console.log(result);
      })
    .catch(error => {
      console.log('error', error)
      });
    sessionStorage.setItem('view', 'sent');
    window.location.reload()
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
      } else if (element.className === 'check-mail col-2'){
        const elementParent = element.parentElement;
        const email_id = elementParent.querySelector('.email_id').innerHTML;
        read_email(email_id);
      } else if (element.className === 'col-2 btn btn-primary'){
        const elementParent = element.parentElement;
        const email_id = elementParent.querySelector('.email_id').innerHTML;
        reply_email(email_id);
      }
  });
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  if (sessionStorage.error === 'Error: Invalid recipient!'){
        
    document.querySelector('#compose-recipients').value = "foo@example.com";
    document.querySelector('#compose-subject').value = "hi";
    document.querySelector('#compose-body').value = "hi"
  }

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#single-mail-view').style.display = 'none';
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
        let check_mail = `<button class="check-mail col-2">Read</button>`;
        if (mailbox == 'sent'){
          sender_or_receiver = `<h5>recipients: ${email['recipients']}</h5>`;
          button = ``;
        };
        if (mailbox === 'archive'){
          button = `<button class="unarchive col-2"> Unarchive </button>`
        };
        contents = sender_or_receiver + contents + `<h6>Timestamp: ${email['timestamp']}</h6>`;
        mail.innerHTML = `${contents} ${button} ${check_mail} `;
        if (email['read'] === true && mailbox == 'inbox'){
          mail.style.backgroundColor = 'grey'
        } else {
          mail.style.backgroundColor = 'white'
        };
        document.querySelector('#emails-view').append(mail);
      });
  })
  .catch(error => {
    console.log('Error:', error);
  });

}

function read_email(email_id){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-mail-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
      // ... do something else with email ...
      const id = email['id'];
      const sender = email['sender'];
      const subject = email['subject'];
      const body = email['body'];
      document.querySelector('#single-mail-view').innerHTML = `<p class="email_id" hidden>${id}<p>  <h4>From: ${sender}</h4> <h4>Subject: ${subject}</h4> <h5>Body: ${body}</h5> <button class="col-2 btn btn-primary">Reply</button>`;
  });
}

function reply_email(email_id){
  //switch to compose email page
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
      // ... do something else with email ...
      const id = email['id'];
      const sender = email['sender'];
      const subject = email['subject'];
      const body = email['body'];
      const timestamp = email['timestamp'];
      //pre-fill the values
      document.querySelector('#compose-recipients').value = sender;
      if (subject.slice(0,4) == "Re: "){
        document.querySelector('#compose-subject').value = subject;
      } else {
        document.querySelector('#compose-subject').value = `Re: ${subject}`;
      }
      document.querySelector('#compose-body').value = `On ${timestamp}, ${sender} wrote: ${body}`;
  });

}