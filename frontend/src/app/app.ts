import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrls: ['./app.scss'],
  standalone: false
})
export class App {
  protected title = 'frontend';
  apiStatusColor = 'black';
  apiLatency = '-';
  dbStatusColor = 'black';
  dbLatency = '-';

  private http = inject(HttpClient);

  constructor() {
    this.checkApiLatency();
    this.checkDbLatency();
    setInterval(() => {
      this.checkApiLatency();
      this.checkDbLatency();
    }, 10000); // update every 10s
  }

  checkApiLatency() {
    const apiUrl = '/api';
    const start = performance.now();
    this.http.get(apiUrl, { observe: 'response' })
      .subscribe({
        next: () => {
          const latency = performance.now() - start;
          this.apiLatency = latency.toFixed(0) + '';
          this.apiStatusColor = latency < 300 ? 'green' : latency < 1000 ? 'yellow' : 'red';
        },
        error: () => {
          this.apiStatusColor = 'red';
          this.apiLatency = '-';
        }
      });
  }

  checkDbLatency() {
    const dbUrl = '/api/genres';
    const start = performance.now();
    this.http.get(dbUrl, { observe: 'response' })
      .subscribe({
        next: () => {
          const latency = performance.now() - start;
          this.dbLatency = latency.toFixed(0) + '';
          this.dbStatusColor = latency < 300 ? 'green' : latency < 1000 ? 'yellow' : 'red';
        },
        error: () => {
          this.dbStatusColor = 'red';
          this.dbLatency = '-';
        }
      });
  }
}
