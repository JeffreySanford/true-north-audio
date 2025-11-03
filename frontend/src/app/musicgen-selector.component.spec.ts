import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { HttpClientModule } from '@angular/common/http';
import { MusicgenEngineSelectorComponent } from './musicgen-selector.component';

describe('MusicgenEngineSelectorComponent', () => {
  let component: MusicgenEngineSelectorComponent;
  let fixture: ComponentFixture<MusicgenEngineSelectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MusicgenEngineSelectorComponent],
      imports: [FormsModule, MatFormFieldModule, MatSelectModule, HttpClientModule]
    }).compileComponents();

    fixture = TestBed.createComponent(MusicgenEngineSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have default engines', () => {
    expect(component.engines.length).toBeGreaterThan(0);
  });

  it('should update selectedEngine', () => {
    const testEngine = component.engines[1];
    component.selectedEngine = testEngine;
    expect(component.selectedEngine).toBe(testEngine);
  });
});
