import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MusicGenController } from '../audio-asset/musicgen.controller';
import { MusicGenService } from '../audio-asset/musicgen.service';
import { HttpModule } from '@nestjs/axios';

@Module({
  imports: [HttpModule],
  controllers: [AppController, MusicGenController],
  providers: [AppService, MusicGenService],
})
export class AppModule {}
