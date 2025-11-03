import { Injectable, OnModuleInit } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import * as fs from 'fs';
import * as path from 'path';
import { Genre, GenreDocument } from './schemas/genre.schema';
import { Instrument, InstrumentDocument } from './schemas/instrument.schema';

@Injectable()
export class GenreSeederService implements OnModuleInit {
  constructor(
    @InjectModel(Genre.name) private genreModel: Model<GenreDocument>,
    @InjectModel(Instrument.name) private instrumentModel: Model<InstrumentDocument>
  ) {}

  async onModuleInit() {
    const genresPath = path.resolve(__dirname, '../../../../ai-music-gen/config/genres.json');
    const genresData = JSON.parse(fs.readFileSync(genresPath, 'utf8'));
    const genres = genresData.genres;

    // Seed genres
    for (const key of Object.keys(genres)) {
      const genre = genres[key];
      await this.genreModel.updateOne(
        { name: genre.name },
        { $set: genre },
        { upsert: true }
      );
      // Seed instruments for each genre
      for (const inst of genre.instruments) {
        await this.instrumentModel.updateOne(
          { name: inst },
          { $set: { name: inst } },
          { upsert: true }
        );
      }
    }
  }
}
