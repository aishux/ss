// If you want to run this code on the client side without using npm and axios, you can use the fetch API, which is available in modern web browsers. Here's the equivalent JavaScript code for the client-side:

document.addEventListener("DOMContentLoaded", function () {
  const myForm = document.getElementById("myForm");
  const LOGINUSERNAME = 'ad';
  const PASSWORD = 'pwd';
  const kURL = 'https://google.com';
  let SESSIONID = '';

  myForm.addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get the userGPN value from the form input
    const userGPN = document.getElementById("userGPN").value;

    // Call the DELETE function with userGPN
    await DELETE(userGPN);
  });

  async function DELETE(USERGPN) {
    try {
      const response = await fetch(`${kURL}/rest/login`, {
        method: 'POST',
        headers: {
          'Accept': 'application/JSON',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${LOGINUSERNAME}&password=${PASSWORD}`,
      });

      if (response.ok) {
        const output = await response.json();
        const LENTOREAD = output.length - 27;
        SESSIONID = output.substring(25, 25 + LENTOREAD);
      }
    } catch (error) {
      console.error(error.message);
      return;
    }

    try {
      const response = await fetch(`${kURL}/rest/user/${USERGPN}`, {
        method: 'DELETE',
        headers: {
          'Accept': 'application/JSON',
          'sessionid': SESSIONID,
        },
      });

      if (response.ok) {
        const output = await response.text();
        console.log(output);
      } else {
        console.error('Failed to delete user.');
      }
    } catch (error) {
      console.error(error.message);
    }
  }
});

