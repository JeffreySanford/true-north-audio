import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { Genre, GenreSchema } from './schemas/genre.schema';
import { Instrument, InstrumentSchema } from './schemas/instrument.schema';
import { GenreSeederService } from './seed-genres';

@Module({
  imports: [
    MongooseModule.forFeature([
      { name: Genre.name, schema: GenreSchema },
      { name: Instrument.name, schema: InstrumentSchema }
    ])
  ],
  providers: [GenreSeederService],
})
export class MusicgenModule {}
