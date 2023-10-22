const LOGINUSERNAME = 'ad';
const PASSWORD = 'pwd';
const kURL = 'https://google.com';
let SESSIONID = '';
const USERGPN = 'your_user_gpn_here'; // Replace with the desired user GPN.

async function getSessionIdFromServer() {
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
  }
}

async function DELETE() {
  await getSessionIdFromServer();
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
    }
  } catch (error) {
    console.error(error.message);
  }
}

DELETE();
