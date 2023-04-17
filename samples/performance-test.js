import http from 'k6/http';
import { check, sleep } from 'k6';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';

// init context: define k6 options
export const options = {
    stages: [
      { duration: '10s', target: 5 },
      { duration: '20s', target: 15 },
      { duration: '20s', target: 25 },
      { duration: '20s', target: 35 },
      { duration: '20s', target: 45 },
      { duration: '20s', target: 80 },
      { duration: '20s', target: 100 },
      { duration: '20s', target: 0 },
    ],
};
const zipFile = open('/Users/juan.henao/Documents/UNIANDES/web/misw4204-grupo17-converter/test_files/user.tar.bz2', 'b');

export default function () {
  let res = http.post('http://127.0.0.1:5001/login', JSON.stringify({username: 'admin', password: 'admin'}), {
    headers: { 'Content-Type': 'application/json' },
  } );
  check(res, {
    'is status 200': (r) => r.status === 200, 
  });

  let authorizationHeader = `Bearer ${res.json().accessToken}`;
  const fd = new FormData();
  fd.append('newFormat', '.zip');
  fd.append('file', http.file(zipFile, 'user.tar.bz2', 'application/tar'));

  let resFile = http.post('http://127.0.0.1:5001/tasks', fd.body(), {
    headers: { 
      'Content-Type': 'multipart/form-data; boundary=' + fd.boundary,
      'Accept-Encoding': 'gzip, deflate, br',
      'Authorization': authorizationHeader
    },
  });
  console.log(resFile.status);
  console.log(resFile.json());

  sleep(1);
}