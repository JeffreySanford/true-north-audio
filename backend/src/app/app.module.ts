import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MusicGenController } from '../audio-asset/musicgen.controller';
import { GenreController } from '../genre/genre.controller';
import { GenreService } from '../genre/genre.service';
import { MusicGenService } from '../audio-asset/musicgen.service';
import { HttpModule } from '@nestjs/axios';
import { SeedService } from './seed.service';
import { MongooseModule } from '@nestjs/mongoose';
import { GenreSchema } from '../models/genre.model';
import { AudioAssetSchema } from '../models/audio-asset.model';

import { MongoMemoryServer } from 'mongodb-memory-server';

const mongooseModule =
  process.env.NODE_ENV === 'development' || process.env.NODE_ENV === 'test'
    ? MongooseModule.forRootAsync({
        useFactory: async () => {
          const mongoServer = await MongoMemoryServer.create();
          return {
            uri: mongoServer.getUri(),
          };
        },
      })
    : MongooseModule.forRoot('mongodb://localhost:27017/true-north-audio');

@Module({
  imports: [
    HttpModule,
    mongooseModule,
    MongooseModule.forFeature([
      { name: 'Genre', schema: GenreSchema },
      { name: 'AudioAsset', schema: AudioAssetSchema },
    ]),
  ],
  controllers: [AppController, MusicGenController, GenreController],
  providers: [AppService, MusicGenService, SeedService, GenreService],
})
export class AppModule {}
