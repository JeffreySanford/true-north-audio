import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.html',
  styleUrls: ['./header.scss'],
  standalone: false,
})
export class HeaderComponent {
  @Input() title = '';
  @Input() subtitle = '';
  @Input() username = 'user123';
  @Input() realname = 'John Doe';
  userMenuOpen = false;

  toggleUserMenu() {
    this.userMenuOpen = !this.userMenuOpen;
  }
}
