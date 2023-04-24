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
const zipFile = open('../test_files/user.tar.bz2', 'b');

export default function () {
  const baseUrl = 'http://34.75.65.39:5001'
  let res = http.post(`${baseUrl}/login`, JSON.stringify({username: 'admin', password: 'admin'}), {
    headers: { 'Content-Type': 'application/json' },
  } );
  check(res, {
    'is status 200': (r) => r.status === 200, 
  });

  let authorizationHeader = `Bearer ${res.json().accessToken}`;
  const fd = new FormData();
  fd.append('newFormat', '.zip');
  fd.append('file', http.file(zipFile, 'user.tar.bz2', 'application/tar'));

  let resFile = http.post(`${baseUrl}/tasks`, fd.body(), {
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