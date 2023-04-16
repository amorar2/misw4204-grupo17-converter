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
  http.get('https://test.k6.io');
  sleep(1);
}