import { TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { App } from './app';
import { HeaderComponent } from './header';
import { RouterModule } from '@angular/router';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDividerModule } from '@angular/material/divider';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

// HTMLElement is a global type in TypeScript, but if you see errors, ensure your tsconfig includes "dom" in "lib"

describe('App', () => {
  beforeEach(async () => {
    // Mock global fetch for tests
    (global as Partial<typeof global>).fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({}),
        headers: new Headers(),
        status: 200,
        statusText: 'OK',
        type: 'basic',
        url: '',
        clone: () => ({
          ok: true,
          json: () => Promise.resolve({}),
          headers: new Headers(),
          status: 200,
          statusText: 'OK',
          type: 'basic',
          url: '',
          body: null,
          bodyUsed: false,
          redirected: false,
          arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)),
          blob: () => Promise.resolve(new Blob([])),
          formData: () => Promise.resolve(new FormData()),
          text: () => Promise.resolve(''),
        } as Response),
        body: null,
        bodyUsed: false,
        redirected: false,
        arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)),
        blob: () => Promise.resolve(new Blob([])),
        formData: () => Promise.resolve(new FormData()),
        text: () => Promise.resolve(''),
      } as Response)
    );

    await TestBed.configureTestingModule({
      imports: [
        RouterModule.forRoot([]),
        HttpClientTestingModule,
        MatCardModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatIconModule,
        MatSelectModule,
        MatSliderModule,
        MatExpansionModule,
        MatProgressSpinnerModule,
        MatDividerModule,
        FormsModule
      ],
  declarations: [App, HeaderComponent],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    }).compileComponents();
  });

  it('should render app-header component', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const headerDebugEl = fixture.debugElement.query(By.css('app-header'));
    expect(headerDebugEl).toBeTruthy();
  });
});
