import { Controller, Get, Param, Body, Post } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Genre, GenreDocument } from './schemas/genre.schema';
import { GenreDto, ToggleInstrumentDto } from './dto/genre.dto';

@Controller('api/genres')
export class GenreController {
  constructor(
    @InjectModel(Genre.name) private genreModel: Model<GenreDocument>
  ) {}

  @Get()
  async listGenres(): Promise<GenreDto[]> {
    return this.genreModel.find().lean();
  }

  @Get(':name')
  async getGenre(@Param('name') name: string): Promise<GenreDto | null> {
    return this.genreModel.findOne({ name }).lean();
  }

  @Post('toggle-instrument')
  async toggleInstrument(@Body() dto: ToggleInstrumentDto): Promise<GenreDto | null> {
    const genre = await this.genreModel.findOne({ name: dto.genreName });
    if (!genre) throw new Error('Genre not found');
    if (dto.enabled) {
      if (!genre.instruments.includes(dto.instrument)) {
        genre.instruments.push(dto.instrument);
      }
    } else {
      genre.instruments = genre.instruments.filter(i => i !== dto.instrument);
    }
    await genre.save();
    return this.genreModel.findOne({ name: dto.genreName }).lean();
  }

}
