import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
      { duration: '20s', target: 20 },
      { duration: '20s', target: 10 },
      { duration: '20s', target: 0 },
    ],
};

export default function () {
  http.get('http://127.0.0.1:5001');
  sleep(1);
}