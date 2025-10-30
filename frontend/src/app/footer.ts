import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.html',
  styleUrls: ['./footer.scss'],
  standalone: false,
})
export class FooterComponent implements OnInit {
  @Input() apiStatusColor = 'black';
  @Input() apiLatency = '-';
  @Input() dbStatusColor = 'black';
  @Input() dbLatency = '-';
  dateTime = '';

  ngOnInit() {
    this.updateDateTime();
    setInterval(() => this.updateDateTime(), 1000);
  }

  updateDateTime() {
    const now = new Date();
    this.dateTime = now.toLocaleString();
  }
}
