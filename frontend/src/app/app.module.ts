import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatOptionModule } from '@angular/material/core';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatBottomSheetModule } from '@angular/material/bottom-sheet';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDividerModule } from '@angular/material/divider';
import { MatSelectModule } from '@angular/material/select';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSliderModule } from '@angular/material/slider';
import { MatChipsModule } from '@angular/material/chips';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { App } from './app';
import { MainPageComponent } from './main-page';
import { HeaderComponent } from './header';
import { FooterComponent } from './footer';
import { MusicGenMainComponent } from './musicgen-main.component';
import { MusicgenEngineSelectorComponent } from './musicgen-selector.component';

@NgModule({
  declarations: [App, MainPageComponent, HeaderComponent, FooterComponent, MusicGenMainComponent, MusicgenEngineSelectorComponent],
  imports: [
    BrowserModule,
    CommonModule,
    FormsModule,
    HttpClientModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatDividerModule,
    MatSelectModule,
    MatExpansionModule,
    MatSliderModule,
    MatChipsModule,
    MatRadioModule,
    MatButtonModule,
    MatToolbarModule,
    MatOptionModule,
    MatSlideToggleModule,
    MatBottomSheetModule
  ],
  providers: [provideBrowserGlobalErrorListeners()],
  bootstrap: [App],
})
export class AppModule {}
