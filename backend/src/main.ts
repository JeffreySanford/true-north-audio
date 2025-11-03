/**
 * This is not a production server yet!
 * This is only a minimal backend to get started.
 */

import { Logger } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app/app.module';

import { spawn } from 'child_process';

async function bootstrap() {
  // Start FastAPI server
  const fastapiProcess = spawn(
    'python',
    [
      '-m', 'uvicorn',
      'ai_music_gen.musicgen.api:app',
      '--host', '0.0.0.0',
      '--port', '11434',
      '--reload'
    ],
    {
      shell: true,
      stdio: 'inherit',
    }
  );
  fastapiProcess.on('error', (err) => {
    Logger.error('Failed to start FastAPI server:', err);
  });
  fastapiProcess.on('exit', (code, signal) => {
    Logger.warn(`FastAPI server exited with code ${code} and signal ${signal}`);
  });

  const app = await NestFactory.create(AppModule);
  // Enable CORS for Angular frontend
  app.enableCors({
    origin: 'http://localhost:4200',
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE,OPTIONS',
    credentials: true,
  });
  const globalPrefix = 'api';
  app.setGlobalPrefix(globalPrefix);
  const port = process.env.PORT || 3000;
  await app.listen(port);
  Logger.log(
    `🚀 Application is running on: http://localhost:${port}/${globalPrefix}`
  );
}

bootstrap();
