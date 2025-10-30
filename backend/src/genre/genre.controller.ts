import { Controller, Get, Post, Put, Delete, Body, Param } from '@nestjs/common';
import { GenreService } from './genre.service';
import { Genre } from '../models/genre.model';

@Controller('genres')
export class GenreController {
  constructor(private readonly genreService: GenreService) {}


  @Post()
  create(@Body() data: Partial<Genre>) {
    return this.genreService.create(data);
  }


  @Get()
  findAll() {
    return this.genreService.findAll();
  }


  @Get(':id')
  findById(@Param('id') id: string) {
    return this.genreService.findById(id);
  }


  @Put(':id')
  update(@Param('id') id: string, @Body() data: Partial<Genre>) {
    return this.genreService.update(id, data);
  }


  @Delete(':id')
  delete(@Param('id') id: string) {
    return this.genreService.delete(id);
  }
}
