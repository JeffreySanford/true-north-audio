import { platformBrowser } from '@angular/platform-browser';
import { AppModule } from './app/app-module';

console.log('[Frontend] Initialization: Starting Angular platform bootstrap');
platformBrowser()
  .bootstrapModule(AppModule, {
    ngZoneEventCoalescing: true,
  })
  .then(() => {
    console.log('[Frontend] Initialization: Angular AppModule bootstrapped');
  })
  .catch((err) => {
    console.error('[Frontend] Initialization: Bootstrap error', err);
  });
