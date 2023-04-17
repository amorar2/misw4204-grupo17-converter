import http from 'k6/http';
import { check, sleep } from 'k6';

// init context: define k6 options
export const options = {
    stages: [
      { duration: '10s', target: 5 },
      // { duration: '20s', target: 15 },
      // { duration: '20s', target: 25 },
      // { duration: '20s', target: 35 },
      // { duration: '20s', target: 45 },
      // { duration: '20s', target: 20 },
      // { duration: '20s', target: 5 },
      // { duration: '20s', target: 0 },
    ],
};

export default function () {
  // 3. VU code, this code is executed by each virtual user in k6
  // const res = http.get('https://httpbin.test.k6.io/');
  // check(res, { 'status was 200': (r) => r.status == 203 });
  // sleep(1);


  let res = http.post('http://127.0.0.1:5001/login', JSON.stringify({username: 'admin', password: 'admin'}), {
    headers: { 'Content-Type': 'application/json' },
  } );
  check(res, {
    'is status 200': (r) => r.status === 200, 
  });
  http.get('http://127.0.0.1:5001');
  sleep(1);
}