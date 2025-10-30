import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { App } from './app';
import { appRoutes } from './app.routes';
import { NxWelcome } from './nx-welcome';
import { MainPageComponent } from './main-page';

@NgModule({
   declarations: [App, NxWelcome, MainPageComponent],
  imports: [BrowserModule, RouterModule.forRoot(appRoutes)],
  providers: [provideBrowserGlobalErrorListeners()],
  bootstrap: [App],
})
export class AppModule {}
