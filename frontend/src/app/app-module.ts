import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
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
import { App } from './app';
import { MainPageComponent } from './main-page';
import { HeaderComponent } from './header';
import { FooterComponent } from './footer';

@NgModule({
  declarations: [App, MainPageComponent, HeaderComponent, FooterComponent],
  imports: [
    BrowserModule,
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
  ],
  providers: [provideBrowserGlobalErrorListeners()],
  bootstrap: [App],
})
export class AppModule {}
