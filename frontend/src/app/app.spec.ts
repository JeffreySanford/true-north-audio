import { TestBed } from '@angular/core/testing';
import { App } from './app';
import { MainPageComponent } from './main-page';
import { RouterModule } from '@angular/router';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

// HTMLElement is a global type in TypeScript, but if you see errors, ensure your tsconfig includes "dom" in "lib"

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
  imports: [
    RouterModule.forRoot([]),
    HttpClientTestingModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
  MatIconModule,
  FormsModule
  ],
  declarations: [App, MainPageComponent],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    }).compileComponents();
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('h1')?.textContent).toContain(
      'True North Audio'
    );
  });
});
