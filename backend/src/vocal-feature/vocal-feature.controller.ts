import { Controller, Get, Post, Put, Delete, Body, Param } from '@nestjs/common';
import { VocalFeatureService } from './vocal-feature.service';
import { VocalFeature } from '../models/vocal-feature.model';

@Controller('vocal-features')
export class VocalFeatureController {
  constructor(private readonly vocalFeatureService: VocalFeatureService) {}


  @Post()
  create(@Body() data: Partial<VocalFeature>) {
    return this.vocalFeatureService.create(data);
  }


  @Get()
  findAll() {
    return this.vocalFeatureService.findAll();
  }


  @Get(':id')
  findById(@Param('id') id: string) {
    return this.vocalFeatureService.findById(id);
  }


  @Put(':id')
  update(@Param('id') id: string, @Body() data: Partial<VocalFeature>) {
    return this.vocalFeatureService.update(id, data);
  }


  @Delete(':id')
  delete(@Param('id') id: string) {
    return this.vocalFeatureService.delete(id);
  }
}
