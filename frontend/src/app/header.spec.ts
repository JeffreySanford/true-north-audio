import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HeaderComponent } from './header';
import { MatIconModule } from '@angular/material/icon';

describe('HeaderComponent', () => {
  let fixture: ComponentFixture<HeaderComponent>;
  // Removed unused variable 'component'

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HeaderComponent],
      imports: [MatIconModule],
    }).compileComponents();
    fixture = TestBed.createComponent(HeaderComponent);
    fixture.detectChanges();
  });

  it('should render logo image', () => {
    const logoImg = fixture.nativeElement.querySelector('img.logo');
    expect(logoImg).toBeTruthy();
    expect(logoImg.getAttribute('src')).toContain('true-north-audio-logo.svg');
  });
});
